"""Purpose of this file

This file describes the frontend views related to profiles.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from django.utils.translation import gettext_lazy as _

from base.models import Profile


class ProfileView(LoginRequiredMixin, DetailView):
    """Profile view

    This model represents the profiles view of the user.

    Attributes:
        ProfileView.model (Model): The model of the view
        ProfileView.template_name (str): The path to the html template
        ProfileView.context_object_name (str): The context object name
    """
    model = Profile
    template_name = "frontend/profile/profile.html"
    context_object_name = "profile"


class ProfileEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    """Profile view

    This model represents the editing profiles view of the user.

    Attributes:
        ProfileView.model (Model): The model of the view
        ProfileView.template_name (str): The path to the html template
        ProfileView.fields (List[str]): TODO
    """
    model = Profile
    template_name = "frontend/profile/profile_edit.html"
    fields = ['bio', 'pic']

    def get_success_url(self):
        """Success URL

        Returns the url for successful delete.

        return: The url of the content to which the deleted argument
        belonged with tag to the comment section
        rtype: str
        """
        return reverse_lazy('frontend:profile', kwargs={'pk': self.request.user.pk})

    def get_success_message(self, cleaned_data):
        """Success message

        Returns the success message when the profile was updated

        Parameters:
            cleaned_data (TODO):

        return: The success message when the profile was updated
        rtype: __proxy__
        """
        return _("Profile updated")

    def get_object(self, queryset=None):
        """Get object

        Returns the profile object of this user.

        return: the profile object of this user
        rtype: Profile
        """
        return Profile.objects.get(user=self.request.user)
