"""Purpose of this file

This file describes or defines the basic structure of the course book.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Favorite(models.Model):
    """Favorite

    This model represents the favourites. A content can be favoured and will
    be marked for the user.

    :attr Favorite.user: The user who favours the content
    :type Favorite.user: ForeignKey - Profile
    :attr Favorite.course: The course containing the content
    :type Favorite.course: ForeignKey - Course
    :attr Favorite.content: The content which was favoured by the user
    :type Favorite.content: ForeignKey - Content
    """

    user = models.ForeignKey("Profile",
                             verbose_name=_("User"),
                             on_delete=models.CASCADE,
                             related_name="user_favorites")
    course = models.ForeignKey("Course",
                               verbose_name=_("Course"),
                               on_delete=models.CASCADE)
    content = models.ForeignKey("Content",
                                verbose_name=_("Content"),
                                on_delete=models.CASCADE)

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.verbose_name: A human-readable name for the object in singular
        :type Meta.verbose_name: __proxy__
        :attr Meta.verbose_name_plural: A human-readable name for the object in plural
        :type Meta.verbose_name_plural: __proxy__
        """
        verbose_name = _("Favorite")
        verbose_name_plural = _("Favorites")

    def __str__(self):
        """String representation

        Returns the string representation of this object.

        :return: the string representation of this object
        :rtype: str
        """
        return f"{self.user} -> {self.course}: {self.content}"
