from django import template
from django.conf import settings

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
