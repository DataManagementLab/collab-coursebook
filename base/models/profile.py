"""Purpose of this file

This file describes or defines the user in the course book.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    """Profile

    This model represents the profile of the user. A profile contains optionally a
    biography and an image. Furthermore the user can favour courses and will be
    marked on its profile.

    :attr Profile.user: The user of the profile
    :type Profile.user: User
    :attr Profile.bio: The biography of the user
    :type Profile.bio: TextField
    :attr Profile.pic: The profile picture of the user
    :type Profile.pic: ImageField
    :attr Profile.stared_courses: The courses that the user favoured
    :type Profile.stared_courses: ManyToManyField - Course
    """
    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.verbose_name: A human-readable name for the object in singular
        :type Meta.verbose_name: __proxy__
        :attr Meta.verbose_name_plural: A human-readable name for the object in plural
        :type Meta.verbose_name_plural: __proxy__
        """
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")

    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(verbose_name=_("Biography"), blank=True)
    pic = models.ImageField(verbose_name=_("Profile picture"), upload_to="profile_pics", blank=True)
    stared_courses = models.ManyToManyField("Course", verbose_name=_("Stared courses:"),
                                            related_name="staring_users", blank=True)
    accepted_privacy_note = models.BooleanField(verbose_name=_("Accepted privacy note?"),\
         blank=True, default=False)

    def __str__(self):
        """String representation

        Returns the string representation of this object.

        :return: the string representation of this object
        :rtype: str
        """
        return str(self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create user profile

    Creates a user profile.

    :param sender: The user of the profile
    :type sender: User
    :param instance: The user instance to be created
    :type instance: User
    :param created: An indicator if the profile was correctly created
    :type created: bool
    :param kwargs: The keyword arguments
    :type kwargs: Any
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save user profile

    Saves the user profile.

    :param sender: The user of the profile
    :type sender: User
    :param instance: The user instance to be saved
    :type instance: User
    :param kwargs: The keyword arguments
    :type kwargs: Any
    """
    profile = Profile.objects.get(user=instance)
    profile.save()
