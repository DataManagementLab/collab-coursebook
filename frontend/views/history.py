"""Purpose of this file

This file describes the frontend history compare views to the models
which are being tracked by the reversion (versioning) and allows us
to compare the differences between different versions of the same model.
"""
from django.urls import reverse

import reversion

from reversion_compare.views import HistoryCompareDetailView

from base.models import Course

from content.models import ImageContent, TextField, YTVideoContent, PDFContent, Latex


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

    # pylint: disable=too-few-public-methods
    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.abstract: Describes whether this model is an abstract model (class)
        :type Meta.abstract: bool
        """
        abstract = True

    def __init__(self, back_url, history_url):
        """Init

        Constructor. Initialize the back and history url to redirect to the
        page corresponding to the model.

        :param back_url: The url to the main page
        :type back_url: str
        :param history_url:  The url to the main history page
        :type history_url: str
        """
        super().__init__()
        self.back_url = back_url
        self.history_url = history_url

    # pylint: disable=assignment-from-no-return
    def get_context_data(self, **kwargs):
        """Context data

        Returns the context data of the history.

        :param kwargs: The keyword arguments
        :type kwargs: dict

        :return: the context data of the history
        :rtype: Dict[str, Any]
        """
        context = super().get_context_data()
        context['back_url'] = self.get_url(self.back_url)
        context['history_url'] = self.get_url(self.history_url)
        return context

    def get_url(self, value):
        """Content url

        Gets the url to the page related to the given value.

        :param value: The redirection to the page
        :type value: str

        :return: url of the page related to the given value
        :rtype: Optional[str]
        """


class BaseContentHistoryCompareView(BaseHistoryCompareView):
    """Base content history compare view

      This detail view represents the base content history compare view. It defines the default
      configurations  and needed information for all other compare views.
      """

    def get_url(self, value):
        """Content url

        Gets the url to the page related to the given value.

        :param value: The redirection to the page
        :type value: str

        :return: url of the page related to the given value
        :rtype: Optional[str]
        """
        course_id = self.kwargs['course_id']
        topic_id = self.kwargs['topic_id']
        content_id = self.get_object().pk
        return reverse(f'frontend:{value}', args=(course_id, topic_id, content_id,))


class BaseCourseHistoryCompareView(BaseHistoryCompareView):
    """Base course history compare view

      This detail view represents the base course history compare view. It defines the default
      configurations  and needed information for all other compare views.
      """

    def get_url(self, value):
        """Content url

        Gets the url to the page related to the given value.

        :param value: The redirection to the page
        :type value: str

        :return: url of the page related to the given value
        :rtype: Optional[str]
        """
        course_id = self.kwargs['pk']
        return reverse(f'frontend:{value}', args=(course_id,))


class CourseHistoryCompareView(BaseCourseHistoryCompareView):
    """Edit course view

    Displays history of this course to the user.

    :attr CourseHistoryCompareView.model: The model of the view
    :type CourseHistoryCompareView.model: Model
    """
    model = Course

    def __init__(self):
        super().__init__('course', 'course-history')


class ImageHistoryCompareView(BaseContentHistoryCompareView):
    """Image history compare view

    Displays history of this content to the user.

    :attr ImageHistoryCompareView.model: The model of the view
    :type ImageHistoryCompareView.model: Model
    """
    model = ImageContent

    def __init__(self):
        super().__init__('content', 'image-history')


class LatexHistoryCompareView(BaseContentHistoryCompareView):
    """LaTeX history compare view

    Displays history of this content to the user

    :attr LatexHistoryCompareView.model: The model of the view
    :type LatexHistoryCompareView.model: Model
    """
    model = Latex

    def __init__(self):
        super().__init__('content', 'latex-history')


class PdfHistoryCompareView(BaseContentHistoryCompareView):
    """PDF history compare view

    Displays history of this content to the user.

    :attr PdfHistoryCompareView.model: The model of the view
    :type PdfHistoryCompareView.model: Model
    """
    model = PDFContent

    def __init__(self):
        super().__init__('content', 'pdf-history')


class TextfieldHistoryCompareView(BaseContentHistoryCompareView):
    """Text field history compare view

    Displays history of this content to the user.

    :attr TextfieldHistoryCompareView.model: The model of the view
    :type TextfieldHistoryCompareView.model: Model
    """
    model = TextField

    def __init__(self):
        super().__init__('content', 'textfield-history')


class YTVideoHistoryCompareView(BaseContentHistoryCompareView):
    """YouTube history compare view

    Displays history of this content to the user.

    :attr YTVideoHistoryCompareView.model: The model of the view
    :type YTVideoHistoryCompareView.model: Model
    """
    model = YTVideoContent

    def __init__(self):
        super().__init__('content', 'ytvideo-history')
