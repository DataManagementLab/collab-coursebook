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

    Attributes:
        CourseAdmin.list_display (List[str]): Controls which fields are displayed on the
        change list page of the admin
        CourseAdmin.readonly_fields (List[str]): Controls which fields are non-editable
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

    Attributes:
        ContentAdmin.readonly_fields (List[str]): Controls which fields are non-editable
        ContentAdmin.exclude (List[str]): Controls which fields should be excluded from the form
    """
    readonly_fields = ['creation_date']
    exclude = ['preview']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """Comment admin

    Represents the comment model in the admin panel.

    Attributes:
        CommentAdmin.readonly_fields (List[str]): Controls which fields are non-editable
    """
    readonly_fields = ['creation_date', 'last_edit']


@admin.register(CourseStructureEntry)
class CourseStructureAdmin(admin.ModelAdmin):
    """Course structure admin

    Represents the course structure model in the admin panel.

    Attributes:
        CourseStructureAdmin.list_display (List[str]): Controls which fields are displayed
        on the change list page of the admin
        CourseStructureAdmin.list_display_links (List[str]): Controls if and which fields
        in list_display should be linked to the "change" page for an object
        CourseStructureAdmin.list_filter (List[str]): Activates filters in the right
        sidebar of the change list page
    """
    list_display = ['index', 'course', 'topic']
    list_display_links = ['index', 'course', 'topic']
    list_filter = ['course']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    """Favourite admin

    Represents the favourite model in the admin panel.

    Attributes:
        FavoriteAdmin.list_display (List[str]): Controls which fields are displayed on the
        change list page of the admin
        FavoriteAdmin.list_display_links (List[str]): Controls if and which fields in
        list_display should be linked to the "change" page for an object
    """
    list_display = ['user', 'course', 'content']
    list_display_links = ['user', 'course', 'content']


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    """Period admin

    Represents the period model in the admin panel.

    Attributes:
        PeriodAdmin.list_display (List[str]): Controls which fields are displayed on the
        change list page of the admin
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
