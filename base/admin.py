from .models import Profile

from django.contrib import admin


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass
