"""Purpose of this file

This file contains the utility functions used in this module.
"""

from django.utils import timezone

from .models import CourseStructureEntry


def create_topic_and_subtopic_list(topics, course):
    """Create (Sub-)Topics list

    Creates an ordered list of (sub-)topics.

    :param topics: The used topics
    :type topics: list
    :param course: The course
    :type course: Course

    :return: a sorted list of topics
    :rtype: list[tuple[str, int, Any, str]]
    """

    sorted_topics = []

    already_checked_topics = []
    for topic in topics:
        # If a topic is part of a course more than one time: the structure
        # loop below gets the remaining structures
        if topic in already_checked_topics:
            continue
        already_checked_topics.append(topic)
        # pylint: disable=no-member
        # Get all structures (even if the same topic is part of the course more than one time)
        for structure in CourseStructureEntry.objects.filter(
                topic=topic,
                course=course
        ).order_by('index'):
            # 0 if main topic - 1 if subtopic
            is_subtopic = 0
            # for easy use in html template: (is_subtopic, topic)
            struct_index = structure.index.split("/")

            if len(struct_index) > 1:
                index_str = str(struct_index[0]) + "." + str(struct_index[1])
                is_subtopic = 1
            else:
                index_str = str(struct_index[0])

            sorted_topics.append((structure.index, is_subtopic, topic, index_str))

    sorted_topics.sort(key=lambda x: structure_to_tuple(x[0]))
    # return list with tuple (is_subtopic, topic)
    return [(topic[1], topic[2], topic[3]) for topic in sorted_topics]


def structure_to_tuple(structure):
    """Structure to tuple

    Returns the index of structure as a tuple. The index determines if the topic is a
    main topic or a sub topic.

    :param structure: The index of the structure
    :type structure: str

    return: the index of the structure as a tuple
    rtype: tuple[int, int]
    """
    if len(structure.split('/')) <= 1:
        return int(structure.split('/')[0]), 0
    return int(structure.split('/')[0]), int(structure.split('/')[1])


def create_course_from_form(self, form):
    """Course from form

    Creates a new course in the database from the form.

    :param self: The given request
    :type self: request
    :param form: The form
    :type form: Form

    :return: the course object
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
    """User

    Returns the current user.

    :param request: The given request
    :type request: HttpRequest

    :return: the user of the request
    :rtype: user
    """
    return request.user.profile


def check_owner_permission(request, course, messages):
    """Owner permission

    Checks if the logged in user is the owner of the course and returns an according boolean.

    :param request: The given request
    :type request: HttpRequest
    :param course: The course for which it should be checked
    :type course: Course
    :param messages: The messages to be able to set an error message
    :type messages: TODO

    :return: true if the owner has no permission and a message should be displayed
    :rtype: bool
    """
    if get_user(request) not in course.owners.all():
        # back url for no permission page
        messages.error(request, "You don't have permission to do this.", extra_tags="alert-danger")
        return True
    return False
