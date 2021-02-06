from django.contrib.admin.utils import quote
from django.http import Http404
from django.urls import reverse
from reversion.models import Version
from reversion_compare.forms import SelectDiffForm
from reversion_compare.views import HistoryCompareDetailView

from base.models import Course, Content
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

    def __init__(self, back_url, history_url):
        self.back_url = back_url
        self.history_url = history_url

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['back_url'] = self.get_content_url(self.back_url)
        context['history_url'] = self.get_content_url(self.history_url)
        return context

    def get_content_url(self, value):
        """Content url

        Gets the url of the content page.

        :return: url of the content page
        :rtype: Optional[str]
        """
        course_id = self.kwargs['course_id']
        topic_id = self.kwargs['topic_id']
        content_id = self.get_object().pk
        return reverse(f'frontend:{value}', args=(course_id, topic_id, content_id,))


class CourseHistoryCompareView(BaseHistoryCompareView):
    """Edit course view

    Displays history of this course to the user.

    :attr CourseHistoryCompareView.model: The model of the view
    :type CourseHistoryCompareView.model: Model
    """
    model = Course

    def __init__(self):
        super().__init__('content', 'course-history')


class ImageHistoryCompareView(BaseHistoryCompareView):
    """Image history compare view

    Displays history of this content to the user.

    :attr ImageHistoryCompareView.model: The model of the view
    :type ImageHistoryCompareView.model: Model
    """
    model = ImageContent

    def __init__(self):
        super().__init__('content', 'image-history')


class LatexHistoryCompareView(BaseHistoryCompareView):
    """LaTeX history compare view

    Displays history of this content to the user

    :attr LatexHistoryCompareView.model: The model of the view
    :type LatexHistoryCompareView.model: Model
    """
    model = Latex

    def __init__(self):
        super().__init__('content', 'latex-history')


class PdfHistoryCompareView(BaseHistoryCompareView):
    """PDF history compare view

    Displays history of this content to the user.

    :attr PdfHistoryCompareView.model: The model of the view
    :type PdfHistoryCompareView.model: Model
    """
    model = PDFContent

    def __init__(self):
        super().__init__('content', 'pdf-history')


class TextfieldHistoryCompareView(BaseHistoryCompareView):
    """Text field history compare view

    Displays history of this content to the user.

    :attr TextfieldHistoryCompareView.model: The model of the view
    :type TextfieldHistoryCompareView.model: Model
    """
    model = TextField

    def __init__(self):
        super().__init__('content', 'textfield-history')


class YTVideoHistoryCompareView(BaseHistoryCompareView):
    """YouTube history compare view

    Displays history of this content to the user.

    :attr YTVideoHistoryCompareView.model: The model of the view
    :type YTVideoHistoryCompareView.model: Model
    """
    model = YTVideoContent

    def __init__(self):
        super().__init__('content', 'ytvideo-history')
