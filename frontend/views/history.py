"""Purpose of this file

This file describes the frontend history compare views to the models
which are being tracked by the reversion (versioning) and allows us
to compare the differences between different versions of the same model.
"""

from builtins import staticmethod

from django.core import serializers
from django.core.files.base import ContentFile
from django.db import transaction
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _

import reversion
from reversion.models import Version

from reversion_compare.views import HistoryCompareDetailView

from base.models import Course, Content, Topic

from content.models import ImageContent, TextField, YTVideoContent, PDFContent, Latex, CONTENT_TYPES
from export.views import generate_pdf_response


class Reversion:  # pylint: disable=too-few-public-methods
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

        Returns the context data of the history.

        :param kwargs: The keyword arguments
        :type kwargs: dict[str, Any]

        :return: the context data of the history
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
        content = obj.content
        versions = Version.objects.get_for_object(content)
        obj_version1 = versions.get(revision=version1.revision)
        obj_version2 = versions.get(revision=version2.revision)

        diff, has_unfollowed_fields = super().compare(content, obj_version1, obj_version2)
        diff2, has_unfollowed_fields2 = super().compare(obj, version1, version2)

        diff += diff2
        has_unfollowed_fields = has_unfollowed_fields or has_unfollowed_fields2

        if content.attachment is not None:
            attachment = content.attachment
            versions = Version.objects.get_for_object(attachment)
            obj_version1 = versions.get(revision=version1.revision)
            obj_version2 = versions.get(revision=version2.revision)
            diff2, has_unfollowed_fields2 = super().compare(attachment,
                                                            obj_version1,
                                                            obj_version2)
            diff += diff2
            has_unfollowed_fields = has_unfollowed_fields or has_unfollowed_fields2

        return diff, has_unfollowed_fields

    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        """Post

        Submits the form and its its information to revert the current content to a previous state.

        :param request: The given request
        :type request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict[str, Any]

        :return: the redirection to the content page after the reversion was successful
        :rtype: HttpResponseRedirect
        """
        topic_id = self.kwargs['topic_id']
        pk = self.kwargs['pk']  # pylint: disable=invalid-name
        rev_pk = request.POST.get('rev_pk')
        with transaction.atomic(), reversion.create_revision():
            revision_id = Version.objects.get(pk=rev_pk).revision_id

            for version in Version.objects.filter(revision_id=revision_id):
                date_time = version.revision.date_created.strftime("%d. %b. %Y, %H:%M")
                reversion.set_comment(_("Revert to version: {}".format(date_time)))

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
                        pdf = generate_pdf_response(request.user.profile,
                                                    deserialized_obj.object.content)
                        deserialized_obj.object.pdf.save(f"{topic}" + ".pdf", ContentFile(pdf))
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

        Submits the form and its its information to revert the current course to a previous state.

        :param request: The given request
        :type request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict[str, Any]

        :return: the redirection to the content page after the reversion was successful
        :rtype: HttpResponseRedirect
        """
        pk = self.kwargs['pk']  # pylint: disable=invalid-name
        rev_pk = request.POST.get('rev_pk')
        with transaction.atomic(), reversion.create_revision():
            version = Version.objects.get(id=rev_pk)

            date_time = version.revision.date_created.strftime("%d. %b. %Y, %H:%M")
            reversion.set_comment(_("Version: {}".format(date_time)))

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
                      'public', 'images', 'textfield', 'source']

    def __init__(self):
        """Initializer

        Initialize the history compare form with pre configuration for the back and history url to
        redirect to the page corresponding to the model.
        """
        super().__init__('content', 'latex-history')


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
                      'public', 'images', 'textfield', 'source']

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
