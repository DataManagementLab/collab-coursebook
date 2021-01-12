"""Purpose of this file

This file describes the frontend views related to search.
"""

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from base.models import Course, CourseStructureEntry


class SearchView(ListView, LoginRequiredMixin):
    """Search view

    This model represents the search for course and topic titles.

    Attributes:
        SearchView.model (Model): The model of the view
        SearchView.template_name (str): The path to the html template
        SearchView.context_object_name (str): The context object name
    """
    model = Course
    template_name = 'frontend/search.html'
    context_object_name = 'search_data'

    def get_queryset(self):
        """Query set

        Returns the query set of the search.

        return: The query set of the search
        rtype: Dict[str, CourseStructureEntry]
        """
        query = self.request.GET.get('q')
        query = query.strip().lower()
        courses = Course.objects.filter(title__icontains=query)
        course_structure_entries = CourseStructureEntry.objects.filter(topic__title__icontains=query)
        return {'courses': courses, 'course_structure_entries': course_structure_entries}

    def get_context_data(self, *, object_list=None, **kwargs):
        """Context data

        Returns the context data of the search.

        Parameters:
            object_list (TODO):
            kwargs (dict): The keyword arguments
        return: the context data of the search
        rtype: Dict[str, Any]
        """
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q')
        return context
