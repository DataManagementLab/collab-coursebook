from django.db.models.functions import Lower
from django.shortcuts import get_object_or_404
from django.views.generic import ListView

from base.models import Course, Category, Period


class CourseListView(ListView):  # pylint: disable=too-many-ancestors
    """
    Displays the courses page with all available course
    """
    model = Course
    template_name = 'frontend/course_lists/courses.html'
    paginate_by = 9

    context_object_name = 'courses'

    def get_queryset(self):
        """
        returns the list of courses sorted with sorting if a value is given
        :return: list of courses
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

    def get_context_data(self, *, object_list=None, **kwargs):  # pylint: disable=unused-argument
        """
        get context data for template
        :param list object_list: django object list
        :param kwargs: django kwargs
        :return: context
        :rtype: dict
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
    template_name = "frontend/course_lists/courses_category.html"

    def dispatch(self, request, *args, **kwargs):
        self.category = get_object_or_404(Category, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(category=self.category)

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx["category"] = self.category
        return ctx


class CourseListForPeriodView(CourseListView):
    template_name = "frontend/course_lists/courses_period.html"

    def dispatch(self, request, *args, **kwargs):
        self.period = get_object_or_404(Period, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return super().get_queryset().filter(period=self.period)

    def get_context_data(self, *, object_list=None, **kwargs):
        ctx = super().get_context_data(object_list=object_list, **kwargs)
        ctx["period"] = self.period
        return ctx
