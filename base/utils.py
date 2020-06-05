"""
This module contains the utility functions used in this project

"""
from django.utils import timezone

from .models import CourseStructureEntry


def create_topic_and_subtopic_list(topics, course):
    """
    creates an ordered list of (sub-)topics
    :param list topics: used topics
    :param Course course: course
    :return: sorted líst of topics
    :rtype: list
    """
    sorted_topics = []

    already_checked_topics = []
    for topic in topics:
        # if a topic is part of a course more than one time: the structure
        # loop below gets the remaining structures
        if topic in already_checked_topics:
            continue
        already_checked_topics.append(topic)
        # get all structures (even if the same topic is part of the course more than one time)
        for structure in CourseStructureEntry.objects.filter(topic=topic, course=course).order_by(
                'index'):  # pylint: disable=no-member
            is_subtopic = 0  # 0 if main topic - 1 if subtopic
            # for easy use in html template: (is_subtopic, topic)
            struct_index = structure.index.split("/")
            if len(struct_index) > 1:
                indexstr = str(struct_index[0]) + "." + str(struct_index[1])
                is_subtopic = 1
            else:
                indexstr = str(struct_index[0])
            sorted_topics.append((structure.index, is_subtopic, topic, indexstr))
    sorted_topics.sort(key=lambda x: structure_to_tuple(x[0]))
    # return list with tuple (is_subtopic, topic)
    return [(topic[1], topic[2], topic[3]) for topic in sorted_topics]


def structure_to_tuple(structure):
    """
    Returns the structure as a tuple
    :param str structure: the index in the structure
    :return: the structure as a tuple
    """
    if len(structure.split('/'))<=1:
        return (int(structure.split('/')[0]), 0)
    else:
        return (int(structure.split('/')[0]) , int(structure.split('/')[1]))


def create_course_from_form(self, form):
    """
    create a new course in the database from the form
    :param Course self: self
    :param AddAndEditCourseForm form: the form containing course data
    :return: course object
    :rtype: Course
    """
    course = form.save(commit=False)
    course.creation_date = timezone.now()
    course.image = form.cleaned_data['image']
    course.author = get_user(self.request)
    course.save()
    for owner in form.cleaned_data['owner']:
        course.owner.add(owner)
    return course


def get_user(request):
    """
    returns the current user
    :param HttpRequest request: request
    :return: the user of the request
    :rtype: user
    """
    return request.user.profile


def check_owner_permission(request, course, messages):
    """
    Checks if the logged in user is the owner of the course. And returns an according boolean
    :param HttpRequest request: the given request
    :param Course course: the course for which it should be checked
    :param messages: the messages to be able to set an error message
    :return: true if the owner has no permission and a message should be displayed
    :rtype: bool
    """
    if get_user(request) not in course.owners.all():
        # back url for no permission page
        messages.error(request, "You don't have permission to do this.",
                       extra_tags="alert-danger")
        return True
    return False
