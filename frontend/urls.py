from django.urls import path, re_path

from frontend import views

app_name = "frontend"

urlpatterns = [
    path('', views.StartView.as_view(), name="index"),
    path('dashboard/', views.DashboardView.as_view(), name="dashboard"),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name="profile"),
    re_path(r'^courses/(?P<sort>date-new|date-old|title-a|title-z)/$', views.CourseList.as_view(), name='courses-sort'),
    path('courses/', views.CourseList.as_view(), name='courses'),
]
