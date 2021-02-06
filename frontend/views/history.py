from django.http import Http404
from reversion.models import Version
from reversion_compare.forms import SelectDiffForm
from reversion_compare.views import HistoryCompareDetailView

from base.models import Course
from content.models import ImageContent, TextField, YTVideoContent, PDFContent, Latex


class BaseHistoryCompareView(HistoryCompareDetailView):
    """Base history compare view

      This detail view represents the base history compare view. It defines the default
      template and needed information for all other compare views.

      :attr BaseHistoryCompareView.template_name: The path to the html template
      :type BaseHistoryCompareView.template_name: str
      """
    template_name = "frontend/history/history.html"

    # pylint: disable=too-few-public-methods
    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.abstract: Describes whether this model is an abstract model (class)
        :type Meta.abstract: bool
        """
        abstract = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        if self.request.GET:
            form = SelectDiffForm(self.request.GET)
            if not form.is_valid():
                msg = "Wrong version IDs."
                raise Http404(msg)

            # Versions for compare
            version_id1 = form.cleaned_data["version_id1"]
            version_id2 = form.cleaned_data["version_id2"]

            if version_id1 > version_id2:
                # Compare always the newest one (#2) with the older one (#1)
                version_id1, version_id2 = version_id2, version_id1

            # Get revision_id for the related queries
            revision_id1 = Version.objects.filter(id=version_id1).values('revision_id')[0]['revision_id']
            revision_id2 = Version.objects.filter(id=version_id2).values('revision_id')[0]['revision_id']

            # Queries to compare
            queryset1 = Version.objects.filter(revision_id=revision_id1)
            queryset2 = Version.objects.filter(revision_id=revision_id2)

            obj = self.get_object()
            queryset = Version.objects.get_for_object(obj)
            next_version = queryset.filter(pk__gt=version_id2).last()
            prev_version = queryset.filter(pk__lt=version_id1).first()
            compares = []

            # Compare data
            for version1, version2 in zip(queryset1, queryset2):
                # TODO does not work since obj is not a content or image attachment.
                # Need to fix that somehow th get the corresponding object
                compares.append(self.compare(obj, version1, version2))

            print(compares)

            # Next, previous versions
            if next_version:
                next_url = f"?version_id1={version2.id:d}&version_id2={next_version.id:d}"
                context.update({"next_url": next_url})
            if prev_version:
                prev_url = f"?version_id1={prev_version.id:d}&version_id2={version1.id:d}"
                context.update({"prev_url": prev_url})

        return context


class CourseHistoryCompareView(BaseHistoryCompareView):
    """Edit course view

    Displays history of this course to the user.

    :attr CourseHistoryCompareView.model: The model of the view
    :type CourseHistoryCompareView.model: Model
    """
    model = Course


class ImageHistoryCompareView(BaseHistoryCompareView):
    """Image history compare view

    Displays history of this content to the user.

    :attr ImageHistoryCompareView.model: The model of the view
    :type ImageHistoryCompareView.model: Model
    """
    model = ImageContent


class LatexHistoryCompareView(BaseHistoryCompareView):
    """LaTeX history compare view

    Displays history of this content to the user

    :attr LatexHistoryCompareView.model: The model of the view
    :type LatexHistoryCompareView.model: Model
    """
    model = Latex


class PdfHistoryCompareView(BaseHistoryCompareView):
    """PDF history compare view

    Displays history of this content to the user.

    :attr PdfHistoryCompareView.model: The model of the view
    :type PdfHistoryCompareView.model: Model
    """
    model = PDFContent


class TextfieldHistoryCompareView(BaseHistoryCompareView):
    """Text field history compare view

    Displays history of this content to the user.

    :attr TextfieldHistoryCompareView.model: The model of the view
    :type TextfieldHistoryCompareView.model: Model
    """
    model = TextField


class YTVideoHistoryCompareView(BaseHistoryCompareView):
    """YouTube history compare view

    Displays history of this content to the user.

    :attr YTVideoHistoryCompareView.model: The model of the view
    :type YTVideoHistoryCompareView.model: Model
    """
    model = YTVideoContent
