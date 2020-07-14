from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin, CreateView, DeleteView, UpdateView
from django.utils.translation import gettext_lazy as _

from base.models import Course, CourseStructureEntry
from base.utils import create_topic_and_subtopic_list, check_owner_permission
from frontend.forms import AddAndEditCourseForm, FilterAndSortForm


class DuplicateCourseView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """
    Duplicate a course
    """
    model = Course
    template_name = 'frontend/course/duplicate.html'
    form_class = AddAndEditCourseForm
    success_url = reverse_lazy('frontend:dashboard')

    def get_success_message(self, cleaned_data):
        original_course = Course.objects.get(pk=self.get_object().id)
        return _(f"Course '{cleaned_data['title']}' successfully created. All settings and contents of the course '{original_course.title}' were copied.")

    def get_initial(self):
        course_to_duplicate = Course.objects.get(pk=self.get_object().id)
        data = course_to_duplicate.__dict__
        # set data not included in the dict
        data['owners'] = get_user(self.request)
        data['image'] = course_to_duplicate.image
        # this data has the wrong key
        data['category'] = course_to_duplicate.category
        data['period'] = course_to_duplicate.period
        return data

    def form_valid(self, form):
        duplicated_course = form.save()
        original_course = Course.objects.get(pk=self.get_object().id)
        course_structure_entries = CourseStructureEntry.objects.filter(course=original_course)
        # duplicate course structure entries
        for entry in course_structure_entries:
            entry.pk = None
            entry.course = duplicated_course
            entry.save()
        return super().form_valid(form)


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


class EditCourseView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """
    Edit course
    """
    model = Course
    template_name = 'frontend/course/edit.html'
    form_class = AddAndEditCourseForm

    def get_success_url(self):
        course_id = self.get_object().id
        return reverse('frontend:course', args=(course_id,))

    def get_success_message(self, cleaned_data):
        return _(f"Course '{cleaned_data['title']}' successfully edited")


class CourseView(DetailView, FormMixin):  # pylint: disable=too-many-ancestors
    """
    Displays the course detail page
    """
    template_name = 'frontend/course/view.html'
    model = Course
    form_class = FilterAndSortForm
    context_object_name = "course"

    def __init__(self):
        self.sorted_by = 'None'
        self.filtered_by = 'None'
        super().__init__()

    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        """
        Defines what happens after form is posted. Sets object and the checks if form is valid
        :param HttpRequest request: the given request
        :param args: arguments
        :param dict kwargs: key word arguments
        :return: the result from form_valid / form_invalid depending on the result from is_valid
        :rtype:
        """
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        """
        Saves the filters and sorting from the form
        :param FilterAndSortForm form: the form that contains the filter and the sorting
        :return: itself rendered to a response
        :rtype: HttpResponse
        """
        self.sorted_by = form.cleaned_data['sort']
        self.filtered_by = form.cleaned_data['filter']
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        """
        context data for page
        :param dict kwargs: kwargs
        :return: context
        :rtype: dict
        """
        context = super().get_context_data(**kwargs)
        structure_entries = CourseStructureEntry.objects.filter(course=context["course"]).order_by('index')

        topics_recursive = []
        current_topic = None
        for entry in structure_entries:
            index_split = entry.index.split('/')
            # Topic
            if len(index_split) == 1:
                current_topic = {'topic': entry.topic, 'subtopics': []}
                topics_recursive.append(current_topic)
            # Subtopic
            # Only handle up to one subtopic level
            else:
                current_topic["subtopics"].append(entry.topic)

        context["structure"] = topics_recursive


        """# create a list of topics ordered by (sub-)topic and index
        flat_topic_list = create_topic_and_subtopic_list(topics, super().get_object())
        print(flat_topic_list)
        context['topics'] = flat_topic_list
        # create a list of files for each (sub-)topic
        files = []
        for _, topic, _ in flat_topic_list:
            files.append(topic.get_contents(self.sorted_by, self.filtered_by))

        context['files'] = files
        # context['Content'] = Content
        if self.sorted_by is not None:
            context['sorting'] = self.sorted_by
        if self.filtered_by is not None:
            context['filtering'] = self.filtered_by
        
        if self.request.user.is_authenticated:
            context['coursebook_length'] = models.get_coursebook_length(user=get_user(self.request), course=self.object)
            context['coursebook'] = models.get_coursebook(get_user(self.request), self.object)
            missing_topics = [x.title for x in self.object.topic_list.order_by('child_topic__index')
                              if Favourite.objects.filter(user=get_user(self.request),
                                                          course=self.object, topic=x).count() == 0
                              or Favourite.objects.get(user=get_user(self.request),
                                                       course=self.object,
                                                       topic=x).content_list.all().count() == 0]
            context['missing_topics'] = ", ".join(missing_topics)
        """

        return context


class CourseDeleteView(LoginRequiredMixin, DeleteView):  # pylint: disable=too-many-ancestors
    """
    Deletes the user and redirects to course list
    """
    model = Course
    template_name = 'frontend/course/delete_course_confirm.html'

    def get_success_url(self):
        """
        Returns the url to return to after successful delete
        :return: the success url
        :rtype: str
        """
        return reverse_lazy('frontend:dashboard')

    # check if the user is allowed to view the delete page
    def dispatch(self, request, *args, **kwargs):
        """
        overwrites dispatch: check if a user is allowed to visit the page
        :param HttpRequest request: request
        :param args: args
        :param dict kwargs: keyword arguments
        :return: Response to redirect to overview of the course if the user is not owner
        :rtype: HttpResponse
        """
        if check_owner_permission(request, self.get_object(), messages):
            return HttpResponseRedirect(reverse_lazy('frontend:course', args=(self.get_object().id,)))
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """
        when the user clicks the delete button
        :param HttpRequest request: request
        :param args: args
        :param dict kwargs: keyword arguments
        :return: redirect to success url (course list)
        :rtype: HttpResponse
        """

        messages.success(request, "Course '" + self.get_object().title +
                         "' successfully deleted", extra_tags="alert-success")
        return super().delete(self, request, *args, **kwargs)