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
