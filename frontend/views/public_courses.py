"""Purpose of this file

This file describes the frontend views related to public courses.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from base.models import Course, Category, Period


class CourseListView(LoginRequiredMixin, ListView):  # pylint: disable=too-many-ancestors)
    """Course list view

    Displays the courses page with all available course.

    :attr CourseListView.model: The model of the view
    :type CourseListView.model: Model
    :attr CourseListView.template_name: The path to the html template
    :type CourseListView.template_name: str
    :attr CourseListView.paginate_by:  Paginate the displayed list
    :type CourseListView.paginate_by: int
    :attr CourseListView.context_object_name: The context object name
    :type CourseListView.context_object_name: str
    """
    model = Course
    template_name = 'frontend/index.html'
    paginate_by = 9

    context_object_name = 'courses'

    def get_queryset(self):
        """Query set

        Returns the list of courses sorted with sorting if a value is given.

        :return: the list of courses
        :rtype: QuerySet
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
        context = super().get_context_data()
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


class CourseListForCategoryView(CourseListView):  # pylint: disable=too-many-ancestors)
    """Course list for category view

    Displays the courses list for category page.

    :attr CourseListForCategoryView.template_name: The path to the html template
    :type CourseListForCategoryView.template_name: str
    """
    template_name = 'frontend/index.html'

    def dispatch(self, request, *args, **kwargs):
        """Dispatch

        Dispatches the course list for category.

        :param request: The given request
        :type request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict[str, Any]

        :return: the redirection page of the dispatch
        :rtype: HttpResponse
        """
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Query set

        Returns the list of courses with the category.

        :return: the list of courses
        :rtype: QuerySet
        """
        return super().get_queryset().filter(category=self.category)

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
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx["category"] = self.category
        return ctx


class CourseListForPeriodView(CourseListView):  # pylint: disable=too-many-ancestors)
    """Course list for category view

    Displays the courses list for period page.

    :attr CourseListForPeriodView.template_name: The path to the html template
    :type CourseListForPeriodView.template_name: str
    """
    template_name = 'frontend/index.html'

    def dispatch(self, request, *args, **kwargs):
        """Dispatch

        Dispatches the course list for period.

        :param request: The given request
        :type request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict[str, Any]

        :return: the redirection page of the dispatch
        :rtype: HttpResponse
        """
        self.period = get_object_or_404(Period, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        """Query set

        Returns the list of courses with the period.

        :return: the list of courses
        :rtype: QuerySet
        """
        return super().get_queryset().filter(period=self.period)

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
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx["period"] = self.period
        return ctx
