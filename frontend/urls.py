from django.urls import path

from frontend import views

app_name = "frontend"

urlpatterns = [
    path('', views.StartView.as_view(), name="index"),
    path('dashboard/', views.DashboardView.as_view(), name="dashboard"),
    path('profile/<int:pk>/', views.ProfileView.as_view(), name="profile"),
]
