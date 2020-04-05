from django.views.generic import DetailView

from base.models import Profile


class ProfileView(DetailView):
    model = Profile
    template_name = "frontend/profile.html"
    context_object_name = "profile"
