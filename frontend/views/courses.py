"""Purpose of this file

This file describes the frontend views related to courses.
"""

from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from base.models import Course, Category, Period


# pylint: disable=tooCourseView-many-ancestors
class CourseListView(ListView):
    """Course list view

    Displays the courses page with all available course.

    Attributes:
        CourseListView.model (Model): The model of the view
        CourseListView.template_name (str): The path to the html template
        CourseListView.paginate_by (int):  Paginate the displayed list
        CourseListView.context_object_name (str): The context object name
    """
    model = Course
    template_name = 'frontend/course_lists/courses.html'
    paginate_by = 9

    context_object_name = 'courses'

    def get_queryset(self):
        """Query set

        Returns the list of courses sorted with sorting if a value is given

        return: the list of courses
        rtype: QuerySet
        """
        queryset = super().get_queryset()

        if 'sort' in self.kwargs:
            sorting = self.kwargs['sort']
            if sorting == "title-a":
                queryset = Course.objects.order_by(Lower("title"))
            elif sorting == "title-z":
                queryset = Course.objects.order_by(Lower("title").desc())
            elif sorting == "date-new":
                queryset = Course.objects.order_by("-creation_date")
            elif sorting == "date-old":
                queryset = Course.objects.order_by("creation_date")
        return queryset

    # pylint: disable=unused-argument
    def get_context_data(self, *, object_list=None, **kwargs):
        """Context data

        Gets context data for the template.

        Parameters:
            object_list (List): The django object list
            kwargs: The django kwargs

        return: The context
        rtype: dict
        """
        context = super(CourseListView, self).get_context_data()
        if "sort" in self.kwargs:
            sort = self.kwargs['sort']
            if sort == 'title-a':
                context['sort'] = "A-Z"
            elif sort == 'title-z':
                context['sort'] = "Z-A"
            elif sort == 'date-new':
                context['sort'] = "newest"
            elif sort == 'date-old':
                context['sort'] = "oldest"
        return context


class CourseListForCategoryView(CourseListView):
    """Course list for category view

    Displays the courses list for category page.

    Attributes:
        CourseListView.template_name (str): The path to the html template
    """
    template_name = "frontend/course_lists/courses_category.html"

    def dispatch(self, request, *args, **kwargs):
        """Dispatch

        Dispatches the course list for category.

        Parameters:
            request (HttpRequest): The given request
            args: The arguments
            kwargs (dict): The additional arguments

        return: the redirection page of the dispatch
        rtype: HttpResponse
        """
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Query set

        Returns the list of courses with the category.

        return: the list of courses
        rtype: QuerySet
        """
        return super().get_queryset().filter(category=self.category)

    def get_context_data(self, *, object_list=None, **kwargs):
        """Context data

        Gets context data for the template.

        Parameters:
            object_list (List): The django object list
            kwargs: The django kwargs

        return: The context
        rtype: dict
        """
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx["category"] = self.category
        return ctx


class CourseListForPeriodView(CourseListView):
    """Course list for category view

    Displays the courses list for period page.

    Attributes:
        CourseListView.template_name (str): The path to the html template
    """
    template_name = "frontend/course_lists/courses_period.html"

    def dispatch(self, request, *args, **kwargs):
        """Dispatch

        Dispatches the course list for period.

        Parameters:
            request (HttpRequest): The given request
            args: The arguments
            kwargs (dict): The additional arguments

        return: the redirection page of the dispatch
        rtype: HttpResponse
        """
        self.period = get_object_or_404(Period, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Query set

        Returns the list of courses with the pariod.

        return: the list of courses
        rtype: QuerySet
        """
        return super().get_queryset().filter(period=self.period)

    def get_context_data(self, *, object_list=None, **kwargs):
        """Context data

        Gets context data for the template.

        Parameters:
            object_list (List): The django object list
            kwargs: The django kwargs

        return: The context
        rtype: dict
        """
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx["period"] = self.period
        return ctx
