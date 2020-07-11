from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from base.models import Course, CourseStructureEntry


class SearchView(ListView, LoginRequiredMixin):
    """
    Search for course and topic titles
    """
    model = Course
    template_name = 'frontend/search.html'
    context_object_name = 'search_data'

    def get_queryset(self):
        query = self.request.GET.get('q')
        query = query.strip().lower()
        courses = Course.objects.filter(title__icontains=query)
        course_structure_entries = CourseStructureEntry.objects.filter(topic__title__icontains=query)
        return {'courses': courses, 'course_structure_entries': course_structure_entries}

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q')
        return context
