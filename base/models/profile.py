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

    Attributes:
        Profile.user (User): The user of the profile
        Profile.bio (TextField): The biography of the user
        Profile.pic (ImageField): The profile picture of the user
        Profile.stared_courses (ManyToManyField - Course): The courses that the user stared
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    bio = models.TextField(verbose_name=_("Biography"), blank=True)
    pic = models.ImageField(verbose_name=_("Profile picture"), upload_to="profile_pics", blank=True)
    stared_courses = models.ManyToManyField("Course", verbose_name=_("Stared courses:"), related_name="staring_users")

    def __str__(self):
        """String representation

        return: the string representation of this object.
        rtype: str
        """
        return str(self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create user profile

    Creates a user profile

    Parameters:
        sender (TODO):
        instance (TODO):
        created (TODO):
        kwargs (TODO):
    """
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save user profile

    Saves the user profile.

    Parameters:
        sender (TODO):
        instance (profile): TODO
        kwargs (TODO):
    """
    instance.profile.save()  # TODO undefined reference?
