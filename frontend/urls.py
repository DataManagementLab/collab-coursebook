"""Purpose of this file

This file defines the URL mapping.
"""

from django.urls import path, re_path, include

from content.models import CONTENT_TYPES
from export.views import generate_coursebook_response
from frontend import views
from frontend.views.coursebook import add_to_coursebook
from frontend.views.search import SearchView

app_name = "frontend"

urlpatterns = [
    path('',
         views.StartView.as_view(),
         name="index"),
    path('dashboard/',
         views.DashboardView.as_view(),
         name="dashboard"),
    path('search/',
         views.search.SearchView.as_view(),
         name='search'),
    path('profile/<int:pk>/',
         views.ProfileView.as_view(),
         name="profile"),
    path('profile/edit/',
         views.ProfileEditView.as_view(),
         name="profile-edit"),

    path('courses/', include([
        re_path(r'^(?P<sort>date-new|date-old|title-a|title-z)/$',
                views.CourseListView.as_view(),
                name='courses-sort'),
        path('',
             views.CourseListView.as_view(),
             name='courses'),
        path('<int:pk>/', include([
            path('duplicate/',
                 views.course.DuplicateCourseView.as_view(),
                 name='course-duplicate'),
            path('',
                 views.CourseView.as_view(),
                 name='course'),
            path('edit/',
                 views.course.EditCourseView.as_view(),
                 name='course-edit'),
            path('delete/',
                 views.CourseDeleteView.as_view(),
                 name='course-delete'),
            path('coursebook/',
                 generate_coursebook_response,
                 name='coursebook-generate'),
        ])),
        path('<int:course_id>/topic/<int:topic_id>/content/', include([

            re_path(r'add/(?P<type>' + '|'.join([key for key in CONTENT_TYPES.keys()]) + ')/$',
                    views.content.AddContentView.as_view(), name='content-add'),
            path('<int:content_id>/', include([
                path('attachment/<int:imageattachment_id>/<int:pk>',
                     views.content.AttachedImageView.as_view(),
                     name='attachment'),
                path('rate/<int:pk>/',
                     views.rate_content,
                     name='rating'),
                path('comment/<int:pk>/delete/',
                     views.DeleteComment.as_view(),
                     name='comment-delete'),
                path('comment/<int:pk>/edit/',
                     views.EditComment.as_view(),
                     name='comment-edit'),
                path('coursebook/add/',
                     views.coursebook.add_to_coursebook,
                     name='coursebook-add'),
                path('coursebook/remove/',
                     views.coursebook.remove_from_coursebook,
                     name='coursebook-remove'),
            ])),
            path('<pk>/',
                 views.ContentView.as_view(),
                 name='content'),
            path('<pk>/edit/',
                 views.content.EditContentView.as_view(),
                 name='content-edit'),
            path('<pk>/delete/',
                 views.content.DeleteContentView.as_view(),
                 name='content-delete'),
            path('<pk>/read/',
                 views.content.ContentReadingModeView.as_view(),
                 name='content-reading-mode'),
            path('<pk>/textfield-history/',
                 views.content.TextfieldHistoryCompareView.as_view(),
                 name='textfield-history'),
            path('<pk>/ytvideo-history/',
                 views.content.YTVideoHistoryCompareView.as_view(),
                 name='ytvideo-history'),
            path('<pk>/image-history/',
                 views.content.ImageHistoryCompareView.as_view(),
                 name='image-history'),
            path('<pk>/pdf-history/',
                 views.content.PdfHistoryCompareView.as_view(),
                 name='pdf-history'),
            path('<pk>/latex-history/',
                 views.content.LatexHistoryCompareView.as_view(),
                 name='latex-history'),

        ])),
        path('add/',
             views.AddCourseView.as_view(),
             name='add-course'),
    ])),

    path('category/<int:pk>/', include([
        re_path(r'^(?P<sort>date-new|date-old|title-a|title-z)/$',
                views.CourseListForCategoryView.as_view(),
                name='category-courses-sort'),
        path('',
             views.CourseListForCategoryView.as_view(),
             name='category-courses'),
    ])),

    path('period/<int:pk>/', include([
        re_path(r'^(?P<sort>date-new|date-old|title-a|title-z)/$',
                views.CourseListForPeriodView.as_view(),
                name='period-courses-sort'),
        path('',
             views.CourseListForPeriodView.as_view(),
             name='period-courses'),
    ])),
]
