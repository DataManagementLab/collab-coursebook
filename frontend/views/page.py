from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView

from base.models import Period, Category


class StartView(TemplateView):
    template_name = "frontend/index.html"


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "frontend/dashboard.html"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["periods"] = Period.objects.all()
        ctx["categories"] = Category.objects.all()
        return ctx

