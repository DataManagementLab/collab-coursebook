"""Purpose of this file

This file describes the frontend views related to pages.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from base.models import Period, Category


class StartView(TemplateView):
    """Dashboard view

    This model represents the start view.

    Attributes:
        StartView.template_name (str): The path to the html template
    """
    template_name = "frontend/index.html"


class DashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard view

    This model represents the dash board view.

    Attributes:
        DashboardView.template_name (str): The path to the html template
    """
    template_name = "frontend/dashboard.html"

    def get_context_data(self, **kwargs):
        """Context data

        Gets the context data.

        Parameters:
            kwargs (dict): The arguments

        return: The context data
        rtype: dict
        """
        ctx = super().get_context_data(**kwargs)
        ctx["periods"] = Period.objects.all()
        ctx["categories"] = Category.objects.all()
        return ctx
