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

    :attr CourseAdmin.list_display: Controls which fields are displayed on the change
    list page of the admin
    :type CourseAdmin.list_display: List[str]
    :attr CourseAdmin.readonly_fields: Controls which fields are non-editable
    :type CourseAdmin.readonly_fields: List[str]
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
    :type ContentAdmin.readonly_fields: List[str]
    :attr ContentAdmin.exclude: Controls which fields should be excluded from the form
    :type ContentAdmin.exclude: List[str]
    """
    readonly_fields = ['creation_date']
    exclude = ['preview']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment admin

    Represents the comment model in the admin panel.

    :attr CommentAdmin.readonly_fields: Controls which fields are non-editable
    :type CommentAdmin.readonly_fields: List[str]
    """
    readonly_fields = ['creation_date', 'last_edit']


@admin.register(CourseStructureEntry)
class CourseStructureAdmin(admin.ModelAdmin):
    """Course structure admin

    Represents the course structure model in the admin panel.

    :attr CourseAdmin.list_display: Controls which fields are displayed on the change
    list page of the admin
    :type CourseAdmin.list_display: List[str]
    :attr CourseStructureAdmin.list_display_links: Controls if and which fields in list_display
    should be linked to the "change" page for an object
    :type CourseStructureAdmin.list_display_links: List[str]
    :attr CourseStructureAdmin.list_filter: Activates filters in the right sidebar of the change
    list page
    :type CourseStructureAdmin.list_filter: List[str]
    """
    list_display = ['index', 'course', 'topic']
    list_display_links = ['index', 'course', 'topic']
    list_filter = ['course']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Favourite admin

    Represents the favourite model in the admin panel.

    :attr FavoriteAdmin.list_display: Controls which fields are displayed on the change
    list page of the admin
    :type FavoriteAdmin.list_display: List[str]
    :attr FavoriteAdmin.list_display_links: Controls if and which fields in list_display
    should be linked to the "change" page for an object
    :type FavoriteAdmin.list_display_links: List[str]
    """
    list_display = ['user', 'course', 'content']
    list_display_links = ['user', 'course', 'content']


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    """Period admin

    Represents the period model in the admin panel.

    :attr PeriodAdmin.list_display_links: Controls if and which fields in list_display
    should be linked to the "change" page for an object
    :type PeriodAdmin.list_display_links: List[str]
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
