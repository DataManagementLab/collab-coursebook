"""Purpose of this file

This file describes or defines the social interaction in the course book.
"""

from django.db import models
from django.utils.translation import gettext_lazy as _


class Rating(models.Model):
    """Rating

    This model represents the user ratings.

    Attributes:
        Rating.CHOICES (List[Tuple[int, str]]): The choices of the ratings
        which is described as a scala from 1 to 5
        Rating.content (ForeignKey - Content): The content to rate
        Rating.user (ForeignKey - Profile): The user of the rating
        Rating.rating (IntegerField): The rating number
    content: the content the rating is for
    user: the user that gave the rating
    rating: the rating the user gave for the content
    """

    CHOICES = [
        (1, 'Very Bad'),
        (2, 'Bad'),
        (3, 'OK'),
        (4, 'Good'),
        (5, 'Very Good'),
    ]

    content = models.ForeignKey("Content", verbose_name=_("Rated content"),
                                on_delete=models.CASCADE)
    user = models.ForeignKey("Profile", verbose_name=_("Rating user"), on_delete=models.CASCADE)
    rating = models.IntegerField(choices=CHOICES, verbose_name=_("Rating"))

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.verbose_name (__proxy__): A human-readable name for the object in singular
            Meta.verbose_name_plural (__proxy__): A human-readable name for the object in plural
            Meta.unique_together (Tuple[str, str]): Sets of field names that, taken together,
            must be unique
        """
        verbose_name = _("Rating")
        verbose_name_plural = _("Ratings")
        unique_together = ('content', 'user')

    def __str__(self):
        """String representation

        return: the string representation of this object.
        rtype: str
        """
        return f"Rating for {self.content} by {self.user}"


class Comment(models.Model):
    """Comment

    Comment Model that saves user comments for a content.

    Attributes:
        Comment.content (ForeignKey - Content): The content the comment belongs to
        Comment.author (ForeignKey - Profile): The user that made the comment
        Comment.text (TextField): The text for the comment
        Comment.creation_date (DateTimeField): The date the comment was made
        Comment.last_edit (DateTimeField): The date when the comment was last edited
    """
    content = models.ForeignKey("Content", verbose_name=_("Comment for"), on_delete=models.CASCADE,
                                related_name="comments")
    author = models.ForeignKey("Profile", verbose_name=_("Author"),
                               on_delete=models.CASCADE, related_name="comments")

    text = models.TextField(verbose_name=_("Comment Text"))

    creation_date = models.DateTimeField(verbose_name=_('Creation Date'),
                                         blank=True, auto_now_add=True)
    last_edit = models.DateTimeField(blank=True, null=True, auto_now=True)

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.verbose_name (__proxy__): A human-readable name for the object in singular
            Meta.verbose_name_plural (__proxy__): A human-readable name for the object in plural
        """
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")

    def __str__(self):
        """String representation

        return: the string representation of this object.
        rtype: str
        """
        return f'Comment for {self.content} by {self.author}'

    @property
    def edited(self):
        """Edit

        Returns when the rating was last edited in seconds.

        return: when the rating was last edited
        rtype: float
        """
        return (self.last_edit - self.creation_date).total_seconds() > 1
