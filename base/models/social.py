from django.db import models
from django.utils.translation import gettext_lazy as _


class Rating(models.Model):
    """
    Rating Model saves the user rating if content
    content: the content the rating is for
    user: the user that gave the rating
    rating: the rating the user gave for the content
    """
    class Meta:
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")
        unique_together = ('content', 'user')

    CHOICES = [
        (1, 'Very Bad'),
        (2, 'Bad'),
        (3, 'OK'),
        (4, 'Good'),
        (5, 'Very Good'),
    ]
    content = models.ForeignKey("Content", verbose_name=_("Rated content"), on_delete=models.CASCADE)
    user = models.ForeignKey("Profile", verbose_name=_("Raiting user"), on_delete=models.CASCADE)
    rating = models.IntegerField(choices=CHOICES, verbose_name=_("Rating"))

    def __str__(self):
        return f"Rating for {self.content} by {self.user}"


class Comment(models.Model):
    """
    Comment Model that saves user comments for a content
    content: the content the comment belongs to
    creation_date: the date the comment was made
    author: the user that made the comment
    text: the text for the comment
    """
    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    content = models.ForeignKey("Content", verbose_name=_("Comment for"), on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey("Profile", verbose_name=_("Author"), on_delete=models.CASCADE, related_name="comments")

    text = models.TextField(verbose_name=_("Comment Text"))

    creation_date = models.DateTimeField(verbose_name=_('Creation Date'), blank=True, auto_now_add=True)
    last_edit = models.DateTimeField(blank=True, null=True, auto_now=True)

    def __str__(self):
        return f'Comment for {self.content} by {self.author}'

    @property
    def edited(self):
        return (self.last_edit - self.creation_date).seconds > 1
