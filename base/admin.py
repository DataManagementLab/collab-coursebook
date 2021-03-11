"""Purpose of this file

This file describes the available base (Course) content in the admin panel. The contents
are ordered alphabetically. This can be found in the Base section of the admin panel.
Contents can be added to or modified for the various content types.
"""

from django.contrib import admin

from .models import Category, Content, Comment, Course
from .models import CourseStructureEntry, Favorite, Period, Profile
from .models import Rating, Tag, Topic


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Course admin

    Represents the course model in the admin panel.

    :attr CourseAdmin.list_display: Controls which fields are displayed
    :type CourseAdmin.list_display: list[str]
    :attr CourseAdmin.readonly_fields: Controls which fields are non-editable
    :type CourseAdmin.readonly_fields: list[str]
    """
    list_display = ['title', 'category', 'period']
    readonly_fields = ['creation_date']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Category admin

    Represents the category model in the admin panel.
    """


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    """Content admin

    Represents the content model in the admin panel.

    :attr ContentAdmin.readonly_fields: Controls which fields are non-editable
    :type ContentAdmin.readonly_fields: list[str]
    :attr ContentAdmin.exclude: Controls which fields should be excluded
    :type ContentAdmin.exclude: list[str]
    """
    readonly_fields = ['creation_date']
    exclude = ['preview']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment admin

    Represents the comment model in the admin panel.

    :attr CommentAdmin.readonly_fields: Controls which fields are non-editable
    :type CommentAdmin.readonly_fields: list[str]
    """
    readonly_fields = ['creation_date', 'last_edit']


@admin.register(CourseStructureEntry)
class CourseStructureAdmin(admin.ModelAdmin):
    """Course structure admin

    Represents the course structure model in the admin panel.

    :attr CourseAdmin.list_display: Controls which fields are displayed
    :type CourseAdmin.list_display: list[str]
    :attr CourseStructureAdmin.list_display_links: Controls which displayed fields should be linked
    :type CourseStructureAdmin.list_display_links: list[str]
    :attr CourseStructureAdmin.list_filter: Controls the filter options on the sidebar
    :type CourseStructureAdmin.list_filter: list[str]
    """
    list_display = ['index', 'course', 'topic']
    list_display_links = ['index', 'course', 'topic']
    list_filter = ['course']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Favourite admin

    Represents the favourite model in the admin panel.

    :attr FavoriteAdmin.list_display: Controls which fields are displayed
    :type FavoriteAdmin.list_display: list[str]
    :attr FavoriteAdmin.list_display_links: Controls which displayed fields should be linked
    :type FavoriteAdmin.list_display_links: list[str]
    """
    list_display = ['user', 'course', 'content']
    list_display_links = ['user', 'course', 'content']


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    """Period admin

    Represents the period model in the admin panel.

    :attr PeriodAdmin.list_display: Controls which fields are displayed
    :type PeriodAdmin.list_display: list[str]
    """
    list_display = ['title', 'start', 'end']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    """Profile admin

    Represents the profile model in the admin panel.
    """


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    """Rating admin

    Represents the rating model in the admin panel.
    """


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Tag admin

    Represents the tag model in the admin panel.
    """


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    """Topic admin

    Represents the topic model in the admin panel.
    """
