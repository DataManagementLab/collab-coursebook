from django import template
from django.conf import settings

from base.models import Favorite
from collab_coursebook.settings import ALLOW_PUBLIC_COURSE_EDITING_BY_EVERYONE
from content.models import CONTENT_TYPES

register = template.Library()


@register.filter
def message_bootstrap_class(tag):
    """
    Translate django message class into bootstrap class

    :param tag: django message class
    :type tag: str
    :return: bootstrap alert class
    :rtype: str
    """
    print(tag)
    if tag == "error":
        return "alert-danger"
    elif tag == "success":
        return "alert-success"
    elif tag == "warning":
        return "alert-warning"
    return "alert-info"


@register.simple_tag
def footer_info():
    """
    Get footer info from settings
    :return: footer info
    :rtype: dict[str, str]
    """
    return settings.FOOTER_INFO


@register.filter
def count_content(topic_queryset):
    """
    This method counts the contents of the topuics in a queryset
    :param QuerySet topic_queryset: the queryset
    :return: the number of contents
    :rtype: int
    """
    count = 0
    for topic in topic_queryset:
        count += len(topic.get_contents("None", "None"))
    return str(count)


@register.filter
def rev_range(arg):
    """
    return range of review
    :param arg: range
    :return: range of review
    """
    return reversed(range(1, arg + 1))


@register.filter
def content_view(type):
    """
    Get matching view for type
    :param type: type of the content
    :type type: str
    :return: path to matching view for type
    :rtype: str
    """
    if type in CONTENT_TYPES.keys():
        return f"content/view/{type}.html"
    return "content/view/invalid.html"


@register.filter
def content_card(type):
    """
    Get matching view for type
    :param type: type of the content
    :type type: str
    :return: path to matching view for type
    :rtype: str
    """
    if type in CONTENT_TYPES.keys():
        return f"content/cards/{type}.html"
    return "content/cards/blank.html"


@register.filter
def check_edit_course_permission(user, course):
    # either an user is an owner or the course is public and it is allowed to edit public courses
    return (user.profile in course.owners.all()) or (not course.restrict_changes
                                                     and ALLOW_PUBLIC_COURSE_EDITING_BY_EVERYONE)


@register.filter
def is_content_editable(type):
    # TODO: implement check
    return False


@register.inclusion_tag("frontend/course/dropdown_topic.html")
def add_content_button(user, course_id, topic_id):
    """
    generate dropdown-button containing list of available content types
    :param User user: the user
    :param int course_id: id of the course
    :param int topic_id: id of the topic
    :return: dropdown button as html div
    :rtype: dict
    """
    # generate list of tuple (content type, content verbose name) for add content dropdown
    content_data = [(content_type, content_model.DESC) for content_type, content_model in CONTENT_TYPES.items()]
    return {'user': user, 'course_id': course_id, 'topic_id': topic_id, 'content_data': content_data}


@register.filter
def get_coursebook(user, course):
    favorites = Favorite.objects.filter(user=user.profile, course=course)
    coursebook = [favorite.content for favorite in favorites]
    return coursebook
