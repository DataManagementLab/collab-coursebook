from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import gettext_lazy as _

from base.models.content import Course


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(verbose_name=_("Biography"), blank=True)
    pic = models.ImageField(verbose_name=_("Profile picture"), upload_to="profile_pics", blank=True)
    stared_courses = models.ManyToManyField(Course, verbose_name=_("Stared courses:"), related_name="staring_users")

    def __str__(self):
        return str(self.user)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
