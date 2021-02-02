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

    This model represents the profile of the user.

    :attr Profile.user: The user of the profile
    :type Profile.user: User
    :attr Profile.bio: The biography of the user
    :type Profile.bio: TextField
    :attr Profile.pic: The profile picture of the user
    :type Profile.pic: ImageField
    :attr Profile.stared_courses: The courses that the user stared
    :type Profile.stared_courses: ManyToManyField - Course
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(verbose_name=_("Biography"), blank=True)
    pic = models.ImageField(verbose_name=_("Profile picture"), upload_to="profile_pics", blank=True)
    stared_courses = models.ManyToManyField("Course", verbose_name=_("Stared courses:"),
                                            related_name="staring_users")

    def __str__(self):
        """String representation

        Returns he string representation of this object.

        :return: the string representation of this object
        :rtype: str
        """
        return str(self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create user profile

    Creates a user profile

    :param sender: The user of the profile
    :type sender: User
    :param instance: The user instance to be created
    :type instance: User
    :param created: True if the profile was created
    :type created: bool
    :param kwargs: The keyword arguments
    :type kwargs: ANY
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save user profile

    Saves the user profile.

    :param sender: The user of the profile
    :type sender: User
    :param instance: THe user instance to be saved
    :type instance: User
    :param kwargs: The keyword arguments
    :type kwargs: ANY
    """
    # TODO Undefined reference?
    instance.profile.save()
