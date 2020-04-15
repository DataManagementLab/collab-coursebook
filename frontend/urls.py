from django.urls import path, re_path, include

from frontend import views

app_name = "frontend"

urlpatterns = [
    path('', views.StartView.as_view(), name="index"),
    path('dashboard/', views.DashboardView.as_view(), name="dashboard"),

    path('profile/<int:pk>/', views.ProfileView.as_view(), name="profile"),
    path('profile/edit/', views.ProfileEditView.as_view(), name="profile-edit"),

    path('courses/', include([
        re_path(r'^(?P<sort>date-new|date-old|title-a|title-z)/$', views.CourseListView.as_view(),
                name='courses-sort'),
        path('', views.CourseListView.as_view(), name='courses'),
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
