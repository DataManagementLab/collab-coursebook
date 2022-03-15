"""Purpose of this file

This file describes the operation on the data manipulation of the course book.
"""

from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse

from base.models import Course, Favorite, Topic, Content


def add_to_coursebook(request, *args, **kwargs):  # pylint: disable=unused-argument
    """Add to course book

    Adds the given content to the coursebook.

    :param request: The given request
    :type request: HttpRequest
    :param args: The arguments
    :type args: Any
    :param kwargs: The keyword arguments
    :type kwargs: dict[str, Any]

    :return: the redirection to the page after the request was added to the course book
    :rtype: HttpResponseRedirect
    """
    user = request.user.profile
    course = get_object_or_404(Course, pk=kwargs['course_id'])
    topic = get_object_or_404(Topic, pk=kwargs['topic_id'])
    content = get_object_or_404(Content, pk=kwargs['content_id'])

    Favorite.objects.create(content=content, user=user, course=course)
    return HttpResponseRedirect(reverse('frontend:course',
                                        args=(course.id,
                                              topic.id,
                                              content.id,)))

def add_to_coursebook_from_courseview(request, *args, **kwargs):  # pylint: disable=unused-argument
    """Add to course book

    Adds the given content to the coursebook.

    :param request: The given request
    :type request: HttpRequest
    :param args: The arguments
    :type args: Any
    :param kwargs: The keyword arguments
    :type kwargs: dict[str, Any]

    :return: the redirection to the page after the request was added to the course book
    :rtype: HttpResponseRedirect
    """
    user = request.user.profile
    course = get_object_or_404(Course, pk=kwargs['course_id'])
    topic = get_object_or_404(Topic, pk=kwargs['topic_id'])
    content = get_object_or_404(Content, pk=kwargs['content_id'])

    Favorite.objects.create(content=content, user=user, course=course)
    return HttpResponseRedirect(reverse('frontend:course',
                                        args=(course.id,)))


def remove_from_coursebook(request, *args, **kwargs):  # pylint: disable=unused-argument
    """Remove from course book

    Removes the given content to the coursebook.

    :param request: The given request
    :type request: HttpRequest
    :param kwargs: The keyword arguments
    :type kwargs: dict[str, Any]

    :return: the redirection to the page after the request was removed from the course book
    :rtype: HttpResponseRedirect
    """
    user = request.user.profile
    course = get_object_or_404(Course, pk=kwargs['course_id'])
    topic = get_object_or_404(Topic, pk=kwargs['topic_id'])
    content = get_object_or_404(Content, pk=kwargs['content_id'])

    Favorite.objects.filter(course=course, user=user, content=content).delete()
    return HttpResponseRedirect(reverse('frontend:course',
                                        args=(course.id,)))

def remove_from_coursebook_from_courseview(request, *args, **kwargs):  # pylint: disable=unused-argument
    """Remove from course book

    Removes the given content to the coursebook.

    :param request: The given request
    :type request: HttpRequest
    :param kwargs: The keyword arguments
    :type kwargs: dict[str, Any]

    :return: the redirection to the page after the request was removed from the course book
    :rtype: HttpResponseRedirect
    """
    user = request.user.profile
    course = get_object_or_404(Course, pk=kwargs['course_id'])
    topic = get_object_or_404(Topic, pk=kwargs['topic_id'])
    content = get_object_or_404(Content, pk=kwargs['content_id'])

    Favorite.objects.filter(course=course, user=user, content=content).delete()
    return HttpResponseRedirect(reverse('frontend:course',
                                        args=(course.id,)))
