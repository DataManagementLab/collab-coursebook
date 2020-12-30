from .models import Profile, Course, Category, Period, Topic, Content, CourseStructureEntry, Tag, Comment, Rating, Favorite

from django.contrib import admin


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    pass


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ['title', 'category', 'period']
    readonly_fields = ['creation_date']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ['title', 'start', 'end']


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    pass


@admin.register(Content)
class ContentAdmin(admin.ModelAdmin):
    readonly_fields = ['creation_date']
    exclude = ['preview']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    pass


@admin.register(CourseStructureEntry)
class CourseStructureAdmin(admin.ModelAdmin):
    list_display = ['index', 'course', 'topic']
    list_display_links = ['index', 'course', 'topic']
    list_filter = ['course']


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    readonly_fields = ['creation_date', 'last_edit']


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    pass


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['user', 'course', 'content']
    list_display_links = ['user', 'course', 'content']
