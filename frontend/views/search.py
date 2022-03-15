"""Purpose of this file

This file describes the frontend views related to search.
"""

from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin

from base.models import Course, CourseStructureEntry


class SearchView(ListView, LoginRequiredMixin):  # pylint: disable=too-many-ancestors
    """Search view

    This model represents the search for course and topic titles.

    :attr SearchView.model: The model of the view
    :type SearchView.model: Model
    :attr SearchView.template_name: The path to the html template
    :type SearchView.template_name: str
    :attr SearchView.context_object_name: The context object name
    :type SearchView.context_object_name: str
    """
    model = Course
    template_name = 'frontend/search.html'
    context_object_name = 'search_data'

    def get_queryset(self):
        """Query set

        Returns the query set of the search.

        :return: The query set of the search
        :rtype: dict[str, QuerySet[CourseStructureEntry]]
        """
        query = self.request.GET.get('q')
        query = query.strip().lower()
        courses = Course.objects.filter(title__icontains=query)
        course_structure_entries = \
            CourseStructureEntry.objects.filter(topic__title__icontains=query)
        content_list = []
        for entry in CourseStructureEntry.objects.all():
            contents = entry.topic.get_contents('None', 'None').filter(description__icontains=query)
            if contents:
                content_list.append([entry, contents])
        return {'courses': courses, 'course_structure_entries': course_structure_entries,
                'content_list': content_list}

    def get_context_data(self, *, object_list=None, **kwargs):
        """Context data

        Gets the context data of the view which can be accessed in
        the html templates.

        :param object_list: The django object list
        :type object_list: list
        :param kwargs: The additional arguments
        :type kwargs: dict[str, Any]

        :return: the context data
        :rtype: dict[str, Any]
        """
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q')
        return context
