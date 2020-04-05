from django.views.generic import TemplateView


class StartView(TemplateView):
    template_name = "frontend/index.html"


class DashboardView(TemplateView):
    template_name = "frontend/dashboard.html"
