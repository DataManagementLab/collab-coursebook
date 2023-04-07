"""Purpose of this file

This file describes the frontend history compare views to the models
which are being tracked by the reversion (versioning) and allows us
to compare the differences between different versions of the same model.
"""
import re

from builtins import staticmethod

from django.contrib.contenttypes.models import ContentType
from django.core import serializers
from django.core.files.base import ContentFile
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.safestring import SafeString
from django.utils.translation import gettext_lazy as _

import reversion
from reversion.models import Version

from reversion_compare.views import HistoryCompareDetailView

from base.models import Course, Content, Topic

from content.attachment.models import ImageAttachment
from content.models import ImageContent, MDContent, TextField, YTVideoContent, PDFContent, Latex, \
    CONTENT_TYPES

from export.views import generate_pdf_from_latex


class Reversion:
    """Reversion utilities

    This class provides utility operation related to reversion.
    """

    @staticmethod
    def update_comment(request):
        """Update reversion comment

        Gets the comment from the form and updates the comment for the reversion.

        :param request: The given request
        :type request: HttpRequest
        """
        # Reversion comment
        change_log = request.POST.get('change_log')

        # Changes log is not empty set it as comment in reversion,
        # else the default comment message will be used
        if change_log:
            reversion.set_comment(change_log)

    @staticmethod
    def compare_removed_added_attachments(attachments, ins_del, index):
        """Compare removed or added attachments

        Compares newly added or removed attachments which do not have a counterpart in the other
        version and creates a html diff. The value of the indicator is either 'ins' or 'del',
        indicating whether the given attachments were added or removed .

        :param attachments: The newly added or removed attachments
        :type attachments: list
        :param ins_del: Indicator whether the given attachments were added or removed
        :type ins_del: str
        :param index: The index at which the added or removed attachments start
        :type index: int

        :return: A diff containing the added or removed attachments
        :rtype: list(dict(str, any))
        """
        diff = []
        for attachment in attachments:
            field_dict = attachment.field_dict
            for field in ImageAttachment()._meta.fields:
                field_name = field.name
                if field_name in field_dict and field_dict[field_name]:
                    html = SafeString(f'<pre class="highlight"><{ins_del}>'
                                      f'{field_dict[field_name]}</{ins_del}></pre>')
                    diff.append({"field": field, "attachment": index, "diff": html})
            index += 1
        return diff


class BaseHistoryCompareView(HistoryCompareDetailView):
    """Base history compare view

      This detail view represents the base history compare view. It defines the default
      template and needed information for all other compare views.

      :attr BaseHistoryCompareView.template_name: The path to the html template
      :type BaseHistoryCompareView.template_name: str
      """
    template_name = "frontend/history/history.html"

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.abstract: Describes whether this model is an abstract model (class)
        :type Meta.abstract: bool
        """
        abstract = True

    def __init__(self, back_url, history_url):
        """Initializer

        Initialize the history compare form with pre configuration for the back and history url to
        redirect to the page corresponding to the model.

        :param back_url: The url to the main page
        :type back_url: str
        :param history_url: The url to the main history page
        :type history_url: str
        """
        super().__init__()
        self.back_url = back_url
        self.history_url = history_url

    def get_context_data(self, **kwargs):
        """Context data

        Gets the context data of the view which can be accessed in
        the html templates.

        :param kwargs: The additional arguments
        :type kwargs: dict[str, Any]

        :return: the context data
        :rtype: dict[str, Any]
        """
        context = super().get_context_data()
        context['back_url'] = self.get_url(self.back_url)  # pylint: disable=assignment-from-no-return
        context['history_url'] = self.get_url(self.history_url)  # pylint: disable=assignment-from-no-return
        return context

    def get_url(self, value):
        """Content url

        Gets the url to the page related to the given value.

        :param value: The redirection to the page
        :type value: str

        :return: url of the page related to the given value
        :rtype: None or str
        """

    def compare(self, obj, version1, version2):
        """Compare two versions of an object

        Create a generic html diff from the obj between version1 and version2

        :param obj: The object to compare
        :type obj: BaseContentModel
        :param version1: The first version to compare
        :type version1: Version
        :param version2: The second version to compare
        :type version2: Version

        :return: A diff of every changed field values
        :rtype: list(dict(str, any)), bool
        """
        diff, has_unfollowed_fields = super().compare(obj, version1, version2)
        # Remove sequence of ?+ or ?- at the end of the result of the compare which is not
        # relevant for the comparison
        for field in diff:
            field['diff'] = SafeString(re.sub(r'</ins>\n\?[\s^+]*', '</ins>\n', field['diff']))
            field['diff'] = SafeString(re.sub(r'</del>\n\?[\s^-]*', '</del>\n', field['diff']))
        return diff, has_unfollowed_fields


class BaseContentHistoryCompareView(BaseHistoryCompareView):
    """Base content history compare view

      This detail view represents the base content history compare view. It defines the default
      configurations  and needed information for all other compare views.
      Each model should modify the attribute compare_files to declare which fields should be
      compared which allow us more customization for the compare view.
      """

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.abstract: Describes whether this model is an abstract model (class)
        :type Meta.abstract: bool
        """
        abstract = True

    def get_url(self, value):
        """Content url

        Gets the url to the page related to the given value.

        :param value: The redirection to the page
        :type value: str

        :return: url of the page related to the given value
        :rtype: None or str
        """
        course_id = self.kwargs['course_id']
        topic_id = self.kwargs['topic_id']
        content_id = self.get_object().pk
        return reverse(f'frontend:{value}', args=(course_id, topic_id, content_id,))

    def __compare_attachment(self, versions1, versions2):
        """Compare attachment

        Create a generic html differences from the attachments between version 1 and
        version 2.

        :param versions1: The attachments of the first version to compare
        :type versions1: list[Version]
        :param versions2: The attachments of the second version to compare
        :type versions2: list[Version]

        :return: the differences of every changed field values
        :rtype: list[dict[str, any]], bool
        """
        diff = []
        has_unfollowed_fields = False
        index = 1
        for attachment_version1, attachment_version2 in zip(versions1, versions2):
            diff2, has_unfollowed_fields2 = super().compare(ImageAttachment(),
                                                            attachment_version1,
                                                            attachment_version2)
            for field in diff2:
                field['attachment'] = index
            index += 1
            diff += diff2
            has_unfollowed_fields = has_unfollowed_fields or has_unfollowed_fields2

        added_attachments = len(versions2) - len(versions1)
        if added_attachments > 0:
            added_attachments = versions2[-added_attachments:]
            diff += Reversion.compare_removed_added_attachments(added_attachments, 'ins', index)
        elif added_attachments < 0:
            removed_attachments = versions1[added_attachments:]
            diff += Reversion.compare_removed_added_attachments(removed_attachments, 'del', index)
        return diff, has_unfollowed_fields

    def compare(self, obj, version1, version2):
        """Compare two versions of an object

        Create a generic html differences from the obj between version 1 and version 2. The
        purpose of the object ist to retrieve the fields to be compared with the function of
        the compare from the super class.

        :param obj: The object to compare
        :type obj: BaseContentModel
        :param version1: The first version to compare
        :type version1: Version
        :param version2: The second version to compare
        :type version2: Version

        :return: the differences of every changed field values
        :rtype: list(dict(str, any)), bool
        """
        content = obj.content
        versions = Version.objects.get_for_object(content)
        obj_version1 = versions.get(revision=version1.revision)
        obj_version2 = versions.get(revision=version2.revision)

        diff, has_unfollowed_fields = super().compare(content, obj_version1, obj_version2)
        diff2, has_unfollowed_fields2 = super().compare(obj, version1, version2)

        diff += diff2
        has_unfollowed_fields = has_unfollowed_fields or has_unfollowed_fields2

        content_type = ContentType.objects.get(model='imageattachment')

        # Get all image attachments versions from both revisions as list
        compared_attachments = self.__compare_attachment(
            versions1=version1.revision.version_set.filter(
                content_type=content_type
            ).order_by('object_id')[::1],
            versions2=version2.revision.version_set.filter(
                content_type=content_type
            ).order_by('object_id')[::1]
        )

        diff += compared_attachments[0]
        has_unfollowed_fields = has_unfollowed_fields or compared_attachments[1]

        return diff, has_unfollowed_fields

    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        """Post

        Defines the action after a post request.

        :param request: The given request
        :type request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict[str, Any]

        :return: the response after a post request
        :rtype: HttpResponseRedirect
        """
        topic_id = self.kwargs['topic_id']
        pk = self.kwargs['pk']  # pylint: disable=invalid-name
        with transaction.atomic(), reversion.create_revision():
            versions = Version.objects.get(pk=request.POST.get('ver_pk')).revision.version_set.all()

            # revert added attachments
            content = Content.objects.get(pk=pk)
            content_type = ContentType.objects.get(model='imageattachment')
            for attachment in content.ImageAttachments.all():
                if not versions.filter(content_type=content_type, object_id=attachment.pk).exists():
                    attachment.delete()

            for version in versions:
                date_time = version.revision.date_created.strftime("%d. %b. %Y, %H:%M")
                reversion.set_comment(_("Reverted to Version: %s") % date_time)

                for deserialized_obj in serializers.deserialize('json', version.serialized_data):
                    if isinstance(deserialized_obj.object, Content):
                        # Revert deletes author and topic, so set it manually
                        content = Content.objects.get(pk=pk)
                        deserialized_obj.object.author_id = content.author_id
                        deserialized_obj.object.topic_id = content.topic_id
                        deserialized_obj.object.type = content.type
                    elif isinstance(deserialized_obj.object, Latex):
                        deserialized_obj.object.save()
                        topic = Topic.objects.get(pk=topic_id)
                        pdf = generate_pdf_from_latex(request.user.profile,
                                                    deserialized_obj.object.content)
                        deserialized_obj.object.pdf.save(f"{topic}" + ".pdf", ContentFile(pdf))
                    elif isinstance(deserialized_obj.object, ImageAttachment):
                        deserialized_obj.object.content_id = pk
                    deserialized_obj.save()

            content = Content.objects.get(pk=pk)
            content.preview = CONTENT_TYPES.get(content.type) \
                .objects.get(pk=content.pk).generate_preview()
            content.save()

        return HttpResponseRedirect(reverse_lazy(
            'frontend:content',
            args=(self.kwargs['course_id'], topic_id, pk,)))


class BaseCourseHistoryCompareView(BaseHistoryCompareView):
    """Base course history compare view

      This detail view represents the base course history compare view. It defines the default
      configurations  and needed information for all other compare views.
      """

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.abstract: Describes whether this model is an abstract model (class)
        :type Meta.abstract: bool
        """
        abstract = True

    def get_url(self, value):
        """Content url

        Gets the url to the page related to the given value.

        :param value: The redirection to the page
        :type value: str

        :return: url of the page related to the given value
        :rtype: None or str
        """
        course_id = self.kwargs['pk']
        return reverse(f'frontend:{value}', args=(course_id,))

    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        """Post

        Defines the action after a post request.

        :param request: The given request
        :type request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict[str, Any]

        :return: the response after a post request
        :rtype: HttpResponseRedirect
        """
        pk = self.kwargs['pk']  # pylint: disable=invalid-name
        ver_pk = request.POST.get('ver_pk')
        with transaction.atomic(), reversion.create_revision():
            version = Version.objects.get(id=ver_pk)

            date_time = version.revision.date_created.strftime("%d. %b. %Y, %H:%M")
            reversion.set_comment(_("Reverted to Version: %s") % date_time)

            for deserialized_obj in serializers.deserialize('json', version.serialized_data):
                if isinstance(deserialized_obj.object, Course):
                    # Revert deletes category and period, so set it manually
                    course = Course.objects.get(pk=pk)
                    deserialized_obj.object.category_id = course.category_id
                    deserialized_obj.object.period_id = course.period_id
                deserialized_obj.object.save()
        course = Course.objects.get(pk=pk)
        course.save()
        return HttpResponseRedirect(reverse_lazy(
            'frontend:course',
            args=(pk,)))


class CourseHistoryCompareView(BaseCourseHistoryCompareView):
    """Edit course view

    Displays history of this course to the user.

    :attr CourseHistoryCompareView.model: The model of the view
    :type CourseHistoryCompareView.model: Model
    :attr CourseHistoryCompareView.compare_fields: The fields which should be compared
    :type CourseHistoryCompareView.compare_fields: list[str]
    """
    model = Course
    compare_fields = ['title', 'description', 'image', 'topics', 'restrict_changes']

    def __init__(self):
        """Initializer

        Initialize the history compare form with pre configuration for the back and history url to
        redirect to the page corresponding to the model.
        """
        super().__init__('course', 'course-history')


class ImageHistoryCompareView(BaseContentHistoryCompareView):
    """Image history compare view

    Displays history of this content to the user.

    :attr ImageHistoryCompareView.model: The model of the view
    :type ImageHistoryCompareView.model: Model
    :attr ImageHistoryCompareView.compare_fields: The fields which should be compared
    :type ImageHistoryCompareView.compare_fields: list[str]
    """
    model = ImageContent
    compare_fields = ['description', 'language', 'tags', 'readonly',
                      'public', 'image', 'source', 'license']

    def __init__(self):
        """Initializer

        Initialize the history compare form with pre configuration for the back and history url to
        redirect to the page corresponding to the model.
        """
        super().__init__('content', 'image-history')


class LatexHistoryCompareView(BaseContentHistoryCompareView):
    """LaTeX history compare view

    Displays history of this content to the user

    :attr LatexHistoryCompareView.model: The model of the view
    :type LatexHistoryCompareView.model: Model
    :attr LatexHistoryCompareView.compare_fields: The fields which should be compared
    :type LatexHistoryCompareView.compare_fields: list[str]
    """
    model = Latex
    compare_fields = ['description', 'language', 'tags', 'readonly',
                      'public', 'image', 'textfield', 'source', 'license']

    def __init__(self):
        """Initializer

        Initialize the history compare form with pre configuration for the back and history url to
        redirect to the page corresponding to the model.
        """
        super().__init__('content', 'latex-history')


class MDHistoryCompareView(BaseContentHistoryCompareView):
    """Markdown history compare view

    Displays history of this content to the user

    :attr MDistoryCompareView.model: The model of the view
    :type MDHistoryCompareView.model: Model
    :attr MDHistoryCompareView.compare_fields: The fields which should be compared
    :type MDHistoryCompareView.compare_fields: list[str]
    """
    model = MDContent
    compare_fields = ['description', 'language', 'tags', 'readonly',
                      'public', 'image', 'textfield', 'source', 'license']

    def __init__(self):
        """Initializer

        Initialize the history compare form with pre configuration for the back and history url to
        redirect to the page corresponding to the model.
        """
        super().__init__('content', 'md-history')


class PdfHistoryCompareView(BaseContentHistoryCompareView):
    """PDF history compare view

    Displays history of this content to the user.

    :attr PdfHistoryCompareView.model: The model of the view
    :type PdfHistoryCompareView.model: Model
    :attr PdfHistoryCompareView.compare_fields: The fields which should be compared
    :type PdfHistoryCompareView.compare_fields: list[str]
    """
    model = PDFContent
    compare_fields = ['description', 'language', 'tags', 'readonly',
                      'public', 'images', 'pdf', 'source', 'license']

    def __init__(self):
        """Initializer

        Initialize the history compare form with pre configuration for the back and history url to
        redirect to the page corresponding to the model.
        """
        super().__init__('content', 'pdf-history')


class TextfieldHistoryCompareView(BaseContentHistoryCompareView):
    """Text field history compare view

    Displays history of this content to the user.

    :attr TextfieldHistoryCompareView.model: The model of the view
    :type TextfieldHistoryCompareView.model: Model
    :attr TextfieldHistoryCompareView.compare_fields: The fields which should be compared
    :type TextfieldHistoryCompareView.compare_fields: list[str]
    """
    model = TextField
    compare_fields = ['description', 'language', 'tags', 'readonly',
                      'public', 'image', 'textfield', 'source', 'license']

    def __init__(self):
        super().__init__('content', 'textfield-history')


class YTVideoHistoryCompareView(BaseContentHistoryCompareView):
    """YouTube history compare view

    Displays history of this content to the user.

    :attr YTVideoHistoryCompareView.model: The model of the view
    :type YTVideoHistoryCompareView.model: Model
    :attr YTVideoHistoryCompareView.compare_fields: The fields which should be compared
    :type YTVideoHistoryCompareView.compare_fields: list[str]
    """
    model = YTVideoContent
    compare_fields = ['description', 'language', 'tags', 'readonly', 'public', 'images', 'url']

    def __init__(self):
        """Initializer

        Initialize the history compare form with pre configuration for the back and history url to
        redirect to the page corresponding to the model.
        """
        super().__init__('content', 'ytvideo-history')
