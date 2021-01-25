from django.urls import path, re_path, include

from export.views import generate_coursebook_response
from content.models import CONTENT_TYPES
from frontend import views
from frontend.views.search import SearchView
from frontend.views.coursebook import add_to_coursebook, remove_from_coursebook

app_name = "frontend"

urlpatterns = [
    path('', views.StartView.as_view(), name="index"),
    path('dashboard/', views.DashboardView.as_view(), name="dashboard"),
    path('search/', views.search.SearchView.as_view(), name='search'),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name="profile"),
    path('profile/edit/', views.ProfileEditView.as_view(), name="profile-edit"),

    path('courses/', include([
        re_path(r'^(?P<sort>date-new|date-old|title-a|title-z)/$',
                views.CourseListView.as_view(), name='courses-sort'),
        path('', views.CourseListView.as_view(), name='courses'),
        path('<int:pk>/', include([
            path('duplicate/', views.course.DuplicateCourseView.as_view(), name='course-duplicate'),
            path('', views.CourseView.as_view(), name='course'),
            path('edit/', views.course.EditCourseView.as_view(), name='course-edit'),
            path('delete/', views.CourseDeleteView.as_view(), name='course-delete'),
            path('coursebook/', generate_coursebook_response, name='coursebook-generate'),
        ])),
        path('<int:course_id>/topic/<int:topic_id>/content/', include([

            path('add/ImageAttachment/', views.content.AddImageAttachmentView.as_view(), name='attachment-add'),
            re_path(r'add/(?P<type>' + '|'.join([key for key in CONTENT_TYPES.keys()]) + ')/$', views.content.AddContentView.as_view(), name='content-add'),
            path('<int:content_id>/', include([
                path('rate/<int:pk>/', views.rate_content, name='rating'),
                path('comment/<int:pk>/delete/', views.DeleteComment.as_view(), name='comment-delete'),
                path('comment/<int:pk>/edit/', views.EditComment.as_view(), name='comment-edit'),
                path('coursebook/add/', views.coursebook.add_to_coursebook, name='coursebook-add'),
                path('coursebook/remove/', views.coursebook.remove_from_coursebook, name='coursebook-remove'),
            ])),
            path('<pk>/', views.ContentView.as_view(), name='content'),
            path('<pk>/edit/', views.content.EditContentView.as_view(), name='content-edit'),
            path('<pk>/read/', views.content.ContentReadingModeView.as_view(), name='content-reading-mode'),
        ])),
        path('add/', views.AddCourseView.as_view(), name='add-course'),
    ])),

    path('category/<int:pk>/', include([
        re_path(r'^(?P<sort>date-new|date-old|title-a|title-z)/$', views.CourseListForCategoryView.as_view(),
            name='category-courses-sort'),
        path('', views.CourseListForCategoryView.as_view(), name='category-courses'),
    ])),

    path('period/<int:pk>/', include([
        re_path(r'^(?P<sort>date-new|date-old|title-a|title-z)/$', views.CourseListForPeriodView.as_view(),
            name='period-courses-sort'),
        path('', views.CourseListForPeriodView.as_view(), name='period-courses'),
    ])),
]
