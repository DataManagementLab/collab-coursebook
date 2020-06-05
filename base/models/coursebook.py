from django.db import models
from django.utils.translation import gettext_lazy as _


class Favorite(models.Model):
    """
    Saving the favorites of a User per Course & Content
    """
    class Meta:
        verbose_name = _("Favorite")
        verbose_name_plural = _("Favorites")

    user = models.ForeignKey("Profile", verbose_name=_("User"), on_delete=models.CASCADE, related_name="user_favorites")
    course = models.ForeignKey("Course", verbose_name=_("Course"), on_delete=models.CASCADE)
    content = models.ForeignKey("Content", verbose_name=_("Content"), on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} -> {self.course}: {self.content}"
