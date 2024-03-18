"""Purpose of this file

This file describes the frontend views related to pages.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView, FormView

from base.models import Period, Category
from collab_coursebook.settings import DATA_PROTECTION_REQURE_CONFIRMATION
from frontend.forms import AcceptPrivacyNoteForm

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from base.models import Course, Category, Period

class StartView(TemplateView):
    """Dashboard view

    This model represents the start view. The starting view is the starting point
    of this project.

    :attr StartView.template_name: The path to the html template
    :type StartView.template_name: str
    """
    template_name = 'frontend/index.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("frontend:dashboard")
        return super().dispatch(request, *args, **kwargs)
    
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
        context["courses"] = Course.objects.all().filter(public=True)
        return context


class DashboardView(LoginRequiredMixin, TemplateView):
    """Dashboard view

    This model represents the dash board view.

    :attr DashboardView.template_name: The path to the html template
    :type DashboardView.template_name: str
    """
    template_name = "frontend/dashboard.html"

    def dispatch(self, request, *args, **kwargs):
        if DATA_PROTECTION_REQURE_CONFIRMATION \
                and request.user.is_authenticated \
                and not request.user.profile.accepted_privacy_note:
            return redirect(reverse_lazy("frontend:privacy_accept"))
        return super().dispatch(request, *args, **kwargs)

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


class PrivacyNoteView(TemplateView):
    """
    View to access privacy note
    """
    template_name = "frontend/data_protection.html"


class AcceptPrivacyNoteView(LoginRequiredMixin, FormView):
    """
    View to review and accept privacy note
    """
    template_name = "frontend/data_protection_accept.html"
    form_class = AcceptPrivacyNoteForm
    success_url = reverse_lazy("frontend:tutorial")

    def form_valid(self, form):
        profile = self.request.user.profile
        profile.accepted_privacy_note = True
        profile.save()
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated \
                and (
                    not DATA_PROTECTION_REQURE_CONFIRMATION
                    or request.user.profile.accepted_privacy_note
                ):
            return redirect(reverse_lazy("frontend:dashboard"))
        return super().dispatch(request, *args, **kwargs)
