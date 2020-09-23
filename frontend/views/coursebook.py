from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from base.models import Course, Favorite, Topic, Content


def add_to_coursebook(request, *args, **kwargs):
    user = request.user.profile
    course = get_object_or_404(Course, pk=kwargs['course_id'])
    topic = get_object_or_404(Topic, pk=kwargs['topic_id'])
    content = get_object_or_404(Content, pk=kwargs['content_id'])

    Favorite.objects.create(content=content, user=user, course=course)
    return HttpResponseRedirect(reverse('frontend:content', args=(course.id, topic.id, content.id,)))


def remove_from_coursebook(request, *args, **kwargs):
    user = request.user.profile
    course = get_object_or_404(Course, pk=kwargs['course_id'])
    topic = get_object_or_404(Topic, pk=kwargs['topic_id'])
    content = get_object_or_404(Content, pk=kwargs['content_id'])

    Favorite.objects.filter(course=course, user=user, content=content).delete()
    return HttpResponseRedirect(reverse('frontend:content', args=(course.id, topic.id, content.id,)))
