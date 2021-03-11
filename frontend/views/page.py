"""Purpose of this file

This file describes the frontend views related to pages.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from base.models import Period, Category


class StartView(TemplateView):
    """Dashboard view

    This model represents the start view. The starting view is the starting point
    of this project.

    :attr StartView.template_name: The path to the html template
    :type StartView.template_name: str
    """
    template_name = "frontend/index.html"


class DashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard view

    This model represents the dash board view.

    :attr DashboardView.template_name: The path to the html template
    :type DashboardView.template_name: str
    """
    template_name = "frontend/dashboard.html"

    def get_context_data(self, **kwargs):
        """Context data

        Gets the context data of the view which can be accessed in
        the html templates.

        :param kwargs: The additional arguments
        :type kwargs: dict[str, Any]

        :return: the context data
        :rtype: dict[str, Any]
        """
        context = super().get_context_data(**kwargs)
        context["periods"] = Period.objects.all()
        context["categories"] = Category.objects.all()
        return context


class TutorialView(TemplateView):
    """Tutorial view

    This model represents the tutorial view. The tutorial view serves as a
    support to make it easier for the user to deal with the page.

    :attr TutorialView.template_name: The path to the html template
    :type TutorialView.template_name: str
    """
    template_name = "frontend/tutorial.html"
