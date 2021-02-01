"""Purpose of this file

This file describes the configuration of frontend including the templates and tags.
"""

from django import template
from django.conf import settings

from base.models import Favorite
from collab_coursebook.settings import ALLOW_PUBLIC_COURSE_EDITING_BY_EVERYONE
from content.models import CONTENT_TYPES, EMBEDDED_CONTENT_TYPES

register = template.Library()


@register.filter
def message_bootstrap_class(tag):
    """Message bootstrap

    Translate django message class into bootstrap class.

    Parameters:
        tag (str): The django message class

    return: The bootstrap alert class
    rtype: str
    """
    if tag == "error":
        return "alert-danger"
    elif tag == "success":
        return "alert-success"
    elif tag == "warning":
        return "alert-warning"
    return "alert-info"


@register.simple_tag
def footer_info():
    """Footer info

    Gets footer info from settings.

    return: The footer info
    rtype: dict[str, str]
    """
    return settings.FOOTER_INFO


@register.filter
def count_content(topic_queryset):
    """Count content

    This method counts the contents of the topics in a queryset.

    Parameters:
        topic_queryset (QuerySet): The queryset

    return: The number of contents
    rtype: int
    """
    count = 0
    for topic in topic_queryset:
        count += len(topic.get_contents("None", "None"))
    return str(count)


@register.filter
def rev_range(arg):
    """Review range

    Returns range of review.

    Parameters:
        arg (int): The range

    return: range of review
    rtype: Iterator
    """
    return reversed(range(1, arg + 1))


@register.filter
def content_view(content_type):
    """Content view

    Gets matching view for type.

    Parameters:
        content_type (str): The type of the content

    return: The path to the matching view for the type
    rtype: str
    """
    if content_type in CONTENT_TYPES.keys():
        return f"content/view/{content_type}.html"
    return "content/view/invalid.html"


@register.filter
def content_card(content_type):
    """Content card

    Gets the matching view for the type.

    Parameters:
        content_type (str): type of the content

    return: The path to the matching view for the type
    rtype: str
    """
    if content_type in CONTENT_TYPES.keys():
        return f"content/cards/{content_type}.html"
    return "content/cards/blank.html"


@register.filter
def check_edit_course_permission(user, course):
    """Edit course permission

    Checks if either an user is an owner or the course is public and it is allowed
    to edit public courses.

    Parameters:
        user (User): The user to check permission
        course (Course): The course th check permission

    return: True if the course can be edited
    rtype: bool
    """
    return (user.profile in course.owners.all()) or (not course.restrict_changes
                                                     and ALLOW_PUBLIC_COURSE_EDITING_BY_EVERYONE)


@register.filter
def check_edit_content_permission(user, content):
    """Edit content permission

    Checks if either an user is an owner or the user is an super user and it is
    allowed to edit the content.

    Parameters:
        user (User): The user to check permission
        content (Content): The content th check permission

    return: True if the content can be edited
    rtype: bool
    """
    if content.readonly:
        return content.author.pk == user.pk or user.is_superuser
    return True


@register.inclusion_tag("frontend/course/dropdown_topic.html")
def add_content_button(user, course_id, topic_id):
    """Content button

    Generates a dropdown-button containing a list of available content types.

    Parameters:
        user (User): The user
        course_id (int): The id of the course
        topic_id (int): The id of the topic

    return: The dropdown button as html div
    rtype: dict
    """
    # generate list of tuple (content type, content verbose name) for add content dropdown
    content_data = [(content_type, content_model.DESC)
                    for content_type, content_model in CONTENT_TYPES.items()]
    content_data = list(filter(lambda x: x[0] not in EMBEDDED_CONTENT_TYPES, content_data))
    return {'user': user,
            'course_id': course_id,
            'topic_id': topic_id,
            'content_data': content_data}


@register.filter
def get_coursebook(user, course):
    """Get coursebook

    Returns the course book from the from the favourites of the user with the given curse.

    Parameters:
        user (User): The user
        course (Course): The course
    return: the coursebook
    rtype: list
    """
    favorites = Favorite.objects.filter(user=user.profile, course=course)
    coursebook = [favorite.content for favorite in favorites]
    return coursebook
