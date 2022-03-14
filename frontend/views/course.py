"""Purpose of this file

This file describes the frontend views related to course.
"""

import json

from django.contrib.auth import get_user
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin, CreateView, DeleteView, UpdateView
from django.utils.translation import gettext_lazy as _

from base.models import Course, CourseStructureEntry, Topic, Favorite
from base.utils import check_owner_permission

from frontend.forms import AddCourseForm, EditCourseForm, FilterAndSortForm
from frontend.forms.course import TopicChooseForm, CreateTopicForm

from frontend.views.history import Reversion
from frontend.views.json import JsonHandler


class DuplicateCourseView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """Duplicate course view

    Duplicates a course.

    :attr DuplicateCourseView.model: The model of the view
    :type DuplicateCourseView.model: Model
    :attr DuplicateCourseView.template_name: The path to the html template
    :type DuplicateCourseView.template_name: str
    :attr DuplicateCourseView.form_class: The form class of the view
    :type DuplicateCourseView.form_class: Form
    :attr DuplicateCourseView.success_url: Redirection of a successful url
    :type DuplicateCourseView.success_url: __proxy__
    """
    model = Course
    template_name = 'frontend/course/duplicate.html'
    form_class = AddCourseForm

    def get_success_url(self):
        return reverse_lazy('frontend:course-edit-structure', kwargs={'pk': self.object.pk})

    def get_success_message(self, cleaned_data):
        """Success message

        Returns the success message after the duplicating of a new course was successful.

        :param cleaned_data: The cleaned data
        :type cleaned_data: dict

        :return: the success message
        :rtype: __proxy__
        """
        original_course = Course.objects.get(pk=self.get_object().id)
        message = _("Course %(title1)s successfully created. "
                    "All settings and contents of the course %(title)s were copied.") \
                  % {'title1': cleaned_data['title'], 'title': original_course.title}
        return message

    def get_initial(self):
        """Initial

        Returns the current user to the initial of the owner field.

        :return: the initial data
        :rtype: dict[str, Any]
        """
        course_to_duplicate = Course.objects.get(pk=self.get_object().id)
        data = course_to_duplicate.__dict__
        # Set data not included in the dict
        data['owners'] = get_user(self.request)
        data['image'] = course_to_duplicate.image
        # This data has the wrong key
        data['category'] = course_to_duplicate.category
        data['period'] = course_to_duplicate.period
        return data

    def form_valid(self, form):
        """Form validation

        Saves the filters and sorting from the form.

        :param form: The form that contains the filter and the sorting
        :type form: FilterAndSortForm

        :return: itself rendered to a response
        :rtype: HttpResponse
        """
        duplicated_course = form.save()
        original_course = Course.objects.get(pk=self.get_object().id)
        course_structure_entries = CourseStructureEntry.objects.filter(course=original_course)
        # Duplicates the course structure entries
        for entry in course_structure_entries:
            entry.pk = None
            entry.course = duplicated_course
            entry.save()
        return super().form_valid(form)


class AddCourseView(SuccessMessageMixin, LoginRequiredMixin, CreateView):
    """Add course view

    Adds a new course to the database.

    :attr AddCourseView.model: The model of the view
    :type AddCourseView.model: Model
    :attr AddCourseView.template_name: The path to the html template
    :type AddCourseView.template_name: str
    :attr AddCourseView.form_class: The form class of the view
    :type AddCourseView.form_class: Form
    :attr AddCourseView.success_url: Redirection of a successful url
    :type AddCourseView.success_url: __proxy__
    """
    model = Course
    template_name = 'frontend/course/create.html'
    form_class = AddCourseForm

    def get_success_url(self):
        return reverse_lazy('frontend:course-edit-structure', kwargs={'pk': self.object.pk})

    def get_success_message(self, cleaned_data):
        """Success message

        Returns the success message after the addition of a new course was successful.

        :param cleaned_data: The cleaned data
        :type cleaned_data: dict

        :return: the success message
        :rtype: __proxy__
        """
        message = _("Course %(title)s successfully created") % {'title': cleaned_data['title']}
        return message

    def get_initial(self):
        """Initial

        Returns the current user to the initial of the owner field.

        :return: the initial data
        :rtype: dict[str, Any]
        """
        initial = super().get_initial()
        initial['owners'] = get_user(self.request).profile
        return initial


class EditCourseView(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """Edit course view

    Displays the edit course page.

    :attr EditCourseView.model: The model of the view
    :type EditCourseView.model: Model
    :attr EditCourseView.template_name: The path to the html template
    :type EditCourseView.template_name: str
    :attr EditCourseView.form_class: The form class of the view
    :type EditCourseView.form_class: Form
    """
    model = Course
    template_name = 'frontend/course/edit.html'
    form_class = EditCourseForm

    def get_success_url(self):
        """Success URL

        Returns the url for successful editing.

        :return: The url of the content to which the edited argument
        belonged
        :rtype: None or str
        """
        course_id = self.get_object().id
        return reverse('frontend:course', args=(course_id,))

    def get_success_message(self, cleaned_data):
        """Success message

        Returns the success message after the editing was successful.

        :param cleaned_data: The cleaned data
        :type cleaned_data: dict[str, Any]

        return: the success message
        rtype: __proxy__
        """
        message = _("Course %(title)s successfully edited") % {'title': cleaned_data['title']}
        return message

    def post(self, request, *args, **kwargs):
        """Post

        Defines the action after a post request.

        :param request: The given request
        :type request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict[str, Any]

        :return: the response after a post request
        :rtype: HttpResponseRedirect
        """
        # Reversion comment
        Reversion.update_comment(request)
        return super().post(request, *args, **kwargs)


class EditCourseStructureView(DetailView, FormMixin):
    """Edit course structure view

    Displays the edit course structure view with some option to
    reorder the topics, add and create new topics.

    :attr EditCourseStructureView.model: The model of the view
    :type EditCourseStructureView.model: Model
    :attr EditCourseStructureView.template_name: The path to the html template
    :type EditCourseStructureView.template_name:str
    :attr EditCourseStructureView.form_class: The form class of the view
    :type EditCourseStructureView.form_class: Form
    """

    template_name = 'frontend/course/edit_structure.html'
    model = Course
    form_class = CreateTopicForm

    def get_context_data(self, **kwargs):
        """Context data

        Gets the context data of the view which can be accessed in
        the html templates.

        :param kwargs: The additional arguments
        :type kwargs: dict[str, Any]

        :return: the context data
        :rtype: dict[str, Any]
        """
        context = super().get_context_data(**kwargs)
        # Json object representing the topics of this course structure
        json_obj = JsonHandler.topics_structure_to_json(self.object)
        context['structure'] = json.dumps(json_obj)
        context['topics'] = TopicChooseForm
        return context

    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        """Post

        Defines the action after a post request.

        :param request: The given request
        :type request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict[str, Any]

        :return: the response after a post request
        :rtype: HttpResponseRedirect
        """
        self.object = self.get_object()
        form_create_topic = self.get_form()
        if form_create_topic.is_valid():
            # AJAX request
            title = request.POST['title']
            category_id = request.POST['category']
            new_topic = Topic.objects.create(title=title, category_id=category_id)
            sorted_topics = []
            # Ordered by category and title of the topic
            for topic in list(Topic.objects.order_by('category__title', 'title')):
                # Use string representation instead of pure title to distinguish to which
                # category a topic is related to
                sorted_topics.append({'id': topic.id, 'title': topic.__str__()})
            data = {'topic_id': new_topic.id, 'topics': sorted_topics}
            return JsonResponse(data=data)
        return self.form_invalid(form_create_topic)


class CourseView(DetailView, FormMixin):
    """Course list view

    Displays the course detail page.

    :attr CourseView.model: The model of the view
    :type CourseView.model: Model
    :attr CourseView.template_name: The path to the html template
    :type CourseView.template_name:str
    :attr CourseView.form_class: The form class of the view
    :type CourseView.form_class: Form
    :attr CourseView.context_object_name: The context object name
    :type CourseView.context_object_name: str
    """

    template_name = 'frontend/course/view.html'
    model = Course
    form_class = FilterAndSortForm
    context_object_name = "course"

    def __init__(self):
        """Initializer

        Initialize the course view with pre configuration for the sort and filter options
        with default values.
        """
        self.sorted_by = 'None'
        self.filtered_by = 'None'
        super().__init__()

    def get_success_url(self):
        """Success url

        Returns the url to return to after successful deletion.

        :return: the success url
        :rtype: __proxy__
        """
        return reverse_lazy('frontend:dashboard')

    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument
        """Post

        Defines the action after a post request.

        :param request: The given request
        :type request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict[str, Any]

        :return: the response after a post request
        :rtype: HttpResponseRedirect
        """
        # Add/remove favourite
        if request.POST.get('save') is not None:
            # Identify the profile and the course
            profile = get_user(request).profile
            course = get_object_or_404(Course, pk=request.POST.get('course_pk'))
            if request.POST.get('save') == 'true':
                profile.stared_courses.add(course)
            else:
                profile.stared_courses.remove(course)
            return HttpResponse()
        if request.POST.get('course_pk') is not None:
            # Identify the profile and the course
            profile = get_user(request).profile
            course = get_object_or_404(Course, pk=request.POST.get('course_pk'))
            return JsonResponse(data={'save': course in profile.stared_courses.all()})

        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)

        # Edit course structure cancel/save
        if request.is_ajax():
            check = True
            # Update course structure
            topic_list = request.POST.get('topic_list')
            if topic_list:
                json_obj = json.loads(topic_list)
                try:
                    JsonHandler.validate_topics(json_data=json_obj)
                except ValidationError:
                    check = False
                if check:
                    JsonHandler.json_to_topics_structure(self.object, json_obj)

            # Clean unused topics
            ids = request.POST.getlist('ids[]')
            if ids:
                JsonHandler.clean_topics(ids)

            if not check:
                return HttpResponseBadRequest()
            return HttpResponse()

        return self.form_invalid(form)

    def form_valid(self, form):
        """Form validation

        Saves the filters and sorting from the form.

        :param form: The form that contains the filter and the sorting
        :type form: FilterAndSortForm

        :return: Itself rendered to a response
        :rtype: HttpResponse
        """
        self.sorted_by = form.cleaned_data['sort']
        self.filtered_by = form.cleaned_data['filter']
        return self.render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        """Context data

        Gets the context data of the view which can be accessed in
        the html templates.

        :param kwargs: The additional arguments
        :type kwargs: dict[str, Any]

        :return: the context data
        :rtype: dict[str, Any]
        """
        
        course_id = self.get_object().id
        favorite_list = [] # Favorite.objects.filter(course=course_id, user=get_user(self.request).profile)
        context = super().get_context_data(**kwargs)
        structure_entries = CourseStructureEntry. \
            objects.filter(course=context["course"]).order_by('index')
        topics_recursive = []
        current_topic = None
        for favorite in Favorite.objects.filter(course=course_id, user=get_user(self.request).profile):
            favorite_list.append(favorite.content)

        for entry in structure_entries:
            index_split = entry.index.split('/')
            # Topic
            if len(index_split) == 1:
                current_topic = {'topic': entry.topic, 'subtopics': [],
                                 'topic_contents': entry.topic.get_contents(self.sorted_by,
                                                                            self.filtered_by)}
                topics_recursive.append(current_topic)
            # Subtopic
            # Only handle up to one subtopic level
            else:
                current_topic["subtopics"].append({'topic': entry.topic,
                                                   'topic_contents':
                                                       entry.topic.
                                                  get_contents(self.sorted_by, self.filtered_by)})


        context["structure"] = topics_recursive
        context['isCurrentUserOwner'] = self.request.user.profile in context['course'].owners.all()
        context['user'] = self.request.user
        context['favorite'] = favorite_list
        if self.sorted_by is not None:
            context['sorting'] = self.sorted_by
        if self.filtered_by is not None:
            context['filtering'] = self.filtered_by

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


class CourseDeleteView(LoginRequiredMixin, DeleteView):
    """Course delete view

    Deletes the course and redirects to course list.

    :attr CourseDeleteView.model: The model of the view
    :type CourseDeleteView.model: Model
    :attr CourseDeleteView.template_name: The path to the html template
    :type CourseDeleteView.template_name: str
    """
    model = Course
    template_name = 'frontend/course/view.html'

    def get_success_url(self):
        """Success url

        Returns the url to return to after successful deletion.

        :return: the success url
        :rtype: __proxy__
        """
        return reverse_lazy('frontend:dashboard')

    def dispatch(self, request, *args, **kwargs):
        """Dispatch

        Overwrites dispatch: Check if a user is allowed to view the deletepage.

        :param request: The given request
        :type request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict[str, Any]

        :return: the response to redirect to overview of the course if the user is not owner
        :rtype: HttpResponse
        """
        if check_owner_permission(request, self.get_object(), messages):
            return HttpResponseRedirect(reverse_lazy('frontend:course',
                                                     args=(self.get_object().id,)))
        return super().dispatch(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        """Delete

        Deletes the course when the user clicks the delete button.

        :param request: The given request
        :type request: HttpRequest
        :param args: The arguments
        :type args: Any
        :param kwargs: The keyword arguments
        :type kwargs: dict[str, Any]

        :return: the redirect to success url (course list)
        :rtype: HttpResponse
        """
        message = _("Course %(title)s successfully deleted") % {'title': self.get_object().title}
        messages.success(request, message, extra_tags="alert-success")
        return super().delete(self, request, *args, **kwargs)
