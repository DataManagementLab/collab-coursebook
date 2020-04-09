from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic.edit import FormMixin, CreateView
from django.utils.translation import gettext_lazy as _

from base.models import Course
from frontend.forms import AddAndEditCourseForm


class AddCourseView(SuccessMessageMixin, LoginRequiredMixin, CreateView):  # pylint: disable=too-many-ancestors
    """
    Adds a new course to the database
    """
    model = Course
    template_name = 'frontend/course/create.html'
    form_class = AddAndEditCourseForm
    success_url = reverse_lazy('frontend:dashboard')

    def get_success_message(self, cleaned_data):
        return _(f"Course '{cleaned_data['title']}' successfully created")

    def get_initial(self):
        """
        the current user to the initial of the owner field
        :return: the initial data
        :rtype: dict
        """
        initial = super().get_initial()
        initial['owners'] = get_user(self.request).profile
        return initial
