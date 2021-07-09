"""collab_coursebook URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

import django_cas_ng.views

import debug_toolbar

urlpatterns = [
                  path('admin/',
                       admin.site.urls),
                  path('i18n/',
                       include('django.conf.urls.i18n')),
                  path('accounts/login/',
                       django_cas_ng.views.LoginView.as_view(),
                       name='cas_ng_login'),
                  path('accounts/logout/',
                       django_cas_ng.views.LogoutView.as_view(),
                       name='cas_ng_logout'),
                  path('accounts/callback/',
                       django_cas_ng.views.CallbackView.as_view(),
                       name='cas_ng_proxy_callback'),
                  path('',
                       include('frontend.urls', namespace='frontend')),
                  path('i18n/',
                       include('django.conf.urls.i18n')),
                  path('__debug__/',
                       include(debug_toolbar.urls)),
              ] + static(settings.MEDIA_URL,
                         document_root=settings.MEDIA_ROOT)
