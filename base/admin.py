"""Purpose of this file

This file describes the available base (Course) content in the admin panel. The contents are ordered alphabetically. This can
be found in the Base section of the admin panel. Contents can be added to or modified for the various content
types.
"""

from django.contrib import admin

from .models import Category, Content, Comment, Course, CourseStructureEntry, Favorite, Period, Profile
from .models import Rating, Tag, Topic


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'period']
    readonly_fields = ['creation_date']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    readonly_fields = ['creation_date']
    exclude = ['preview']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ['creation_date', 'last_edit']


@admin.register(CourseStructureEntry)
class CourseStructureAdmin(admin.ModelAdmin):
    list_display = ['index', 'course', 'topic']
    list_display_links = ['index', 'course', 'topic']
    list_filter = ['course']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'content']
    list_display_links = ['user', 'course', 'content']


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ['title', 'start', 'end']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass
