"""Purpose of this file

This file describes the configuration of frontend including the templates and tags.
"""

import re

from django import template
from django.conf import settings

from base.models import Favorite

from collab_coursebook.settings import ALLOW_PUBLIC_COURSE_EDITING_BY_EVERYONE

from content.models import CONTENT_TYPES

from datetime import timedelta

register = template.Library()


@register.filter
def message_bootstrap_class(tag):
    """Message bootstrap

    Translate django message class into bootstrap class.

    :param tag: The django message class
    :type tag: str

    :return: the bootstrap alert class
    :rtype: str
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

    :return: the footer info
    :rtype: dict[str, str]
    """
    return settings.FOOTER_INFO


@register.filter
def count_content(topic_queryset):
    """Count content

    This method counts the contents of the topics in a queryset.

    :param topic_queryset: The queryset
    :type topic_queryset: QuerySet[Topic]

    :return: the number of contents
    :rtype: str
    """
    count = 0
    for topic in topic_queryset:
        count += len(topic.get_contents("None", "None"))
    return str(count)


@register.filter
def rev_range(arg):
    """Review range

    Returns range of review.

    :param arg: The range
    :type arg: int

    :return: the range of review
    :rtype: Iterator[_T]
    """
    return reversed(range(1, arg + 1))


@register.filter
def content_view(content_type):
    """Content view

    Gets matching view for type.

    :param content_type: The type of the content
    :type content_type: str

    :return: the path to the matching view for the type
    :rtype: str
    """
    if content_type in CONTENT_TYPES.keys():
        return f"content/view/{content_type}.html"
    return "content/view/invalid.html"


@register.filter
def content_reading(content_type):
    """Content reading

    Gets matching reading view for type.

    :param content_type: The type of the content
    :type content_type: str

    :return: the path to the matching view for the type
    :rtype: str
    """
    if content_type in CONTENT_TYPES.keys():
        return f"content/reading_mode/{content_type}.html"
    return "content/view/invalid.html"


@register.filter
def content_card(content_type):
    """Content card

    Gets the matching view for the type.

    :param content_type: The type of the content
    :type content_type: str

    :return: the path to the matching view for the type
    :rtype: str
    """
    if content_type in CONTENT_TYPES.keys():
        return f"content/cards/{content_type}.html"
    return "content/cards/blank.html"


@register.filter
def check_edit_course_permission(user, course):
    """Edit course permission

    Checks if either an user is an owner or the course is public and it is allowed
    to edit public courses.

    :param user: The user to check permission
    :type user: User
    :param course: The course to check permission
    :type course: Course

    :return: true iff the course can be edited
    :rtype: bool
    """
    return (user.profile in course.owners.all()) or (not course.restrict_changes
                                                     and ALLOW_PUBLIC_COURSE_EDITING_BY_EVERYONE)


@register.filter
def check_delete_course_permission(user, course):
    """Delete course permission

    Checks if either a user is an owner or the course is public and it is allowed
    to edit public courses.

    :param user: The user to check permission
    :type user: User
    :param course: The course to check permission
    :type course: Course

    :return: true iff the course can be deleted by the current user
    :rtype: bool
    """
    return user.profile in course.owners.all()


@register.filter
def check_profile_permissions(user, profile):
    """Check Profile Permission

    Checks if a user is allowed to see the stared courses in the profile of a user

    :param user: The user to check permission
    :type user: User
    :param profile: The profile to check permission
    :type profile: Profile

    :return: true iff the stared courses of the profile can be seen
    :rtype: bool
    """
    return user.profile.pk == profile.pk or user.is_superuser


@register.filter
def check_edit_content_permission(user, content):
    """Edit content permission

    Checks if either an user is an owner or the user is an super user and it is
    allowed to edit the content.

    :param user: The user to check permission
    :type user: User
    :param content: The content to check permission
    :type content: Content

    :return: true iff the content can be edited
    :rtype: bool
    """
    if content.readonly:
        return content.author.pk == user.pk or user.is_superuser
    return True


@register.inclusion_tag("frontend/course/dropdown_topic.html")
def add_content_button(user, course_id, topic_id):
    """Content button

    Generates a dropdown-button containing a list of available content types.

    :param user: The user to check permission
    :type user: User
    :param course_id: The id of the course
    :type course_id: int
    :param topic_id: The id of the topic
    :type topic_id: int

    :return: The dropdown button as html div
    :rtype: dict[str, Any]
    """
    # Generates a list of tuple (content type, content verbose name) for add content dropdown
    content_data = [(content_type, content_model.DESC)
                    for content_type, content_model in CONTENT_TYPES.items()]
    return {'user': user,
            'course_id': course_id,
            'topic_id': topic_id,
            'content_data': content_data}


@register.filter
def get_coursebook(user, course):
    """Get coursebook

    Returns the course book from the from the favourites of the user with the given curse.

    :param user: The user
    :type user: User
    :param course: The course
    :type course: Course

    :return: the coursebook
    :rtype: list[Content]
    """
    favorites = Favorite.objects.filter(user=user.profile, course=course)
    coursebook = [favorite.content for favorite in favorites]
    return coursebook


@register.filter
def format_seconds(seconds):
    """
    This filter converts seconds to a hh:mm:ss format
    Will be used for Panopto integration since start_time is only given in seconds
    """
    try:
        # Try converting as a simple numeric string
        sec = int(float(seconds))
        return str(timedelta(seconds=sec))
    except ValueError:
        # If conversion fails, assume it's already in the format "0:00:00"
        return seconds



def js_escape(value):
    """JavaScript escape

    Escapes the characters from python string to JavaScript string.

    :param value: The string to be escaped
    :type value: str

    :return: the escaped string
    :rtype: str
    """
    # Replacements for left character with right character
    replacements = {
        '\\': '\\\\',
        '\n': '\\n'
    }

    # Compile into pattern objects
    regex = re.compile(
        # Concatenate the escaped characters to one string
        '|'.join(
            # Escape special characters in pattern
            re.escape(key) for key in replacements
        )
    )
    return regex.sub(lambda match: replacements[match.group()], value)
