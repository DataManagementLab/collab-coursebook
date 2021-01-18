"""Purpose of this file

This file describes or defines the basic structure of the course book.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Favorite(models.Model):
    """Favorite

    Saving the favorites of a User per Course & Content

    Attributes:
        Favorite.user (ForeignKey - Profile): Describes favourites of the user
        Favorite.course (ForeignKey - Course): Describes the favourites courses of the user
        Favorite.content (ForeignKey - Content): Describes the favourites contents of the user
    """

    user = models.ForeignKey("Profile", verbose_name=_("User"), on_delete=models.CASCADE,
                             related_name="user_favorites")
    course = models.ForeignKey("Course", verbose_name=_("Course"), on_delete=models.CASCADE)
    content = models.ForeignKey("Content", verbose_name=_("Content"), on_delete=models.CASCADE)

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.verbose_name (__proxy__): A human-readable name for the object in singular
            Meta.verbose_name_plural (__proxy__): A human-readable name for the object in plural
        """
        verbose_name = _("Favorite")
        verbose_name_plural = _("Favorites")

    def __str__(self):
        """String representation

        return: the string representation of this object.
        rtype: str
        """
        return f"{self.user} -> {self.course}: {self.content}"
