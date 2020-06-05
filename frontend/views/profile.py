from dal import autocomplete
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import DetailView, UpdateView
from django.utils.translation import gettext_lazy as _

from base.models import Profile


class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = "frontend/profile/profile.html"
    context_object_name = "profile"


class ProfileEditView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Profile
    template_name = "frontend/profile/profile_edit.html"
    fields = ['bio', 'pic']

    def get_success_url(self):
        return reverse_lazy('frontend:profile', kwargs={'pk': self.request.user.pk})

    def get_success_message(self, cleaned_data):
        return _(f"Profile updated")

    def get_object(self, queryset=None):
        return Profile.objects.get(user=self.request.user)
