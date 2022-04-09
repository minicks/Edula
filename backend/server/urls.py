"""server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

import re


base_api_url = 'api/'
api_version = ''

urlpatterns = [
    # APPs
    path('admin/', admin.site.urls),
    path(base_api_url + api_version + 'accounts/', include('accounts.urls')),
    path(base_api_url + api_version + 'schools/', include('schools.urls')),
    path(base_api_url + api_version + 'notifications/', include('notifications.urls')),
    path(base_api_url + api_version + 'messages/', include('message.urls')),
    path(base_api_url + api_version + 'quiz/', include('quiz.urls')),
    # JWT
    path(
        base_api_url + api_version + 'token/',
        TokenObtainPairView.as_view(),
        name='JWT_login',
    ),
    path(
        base_api_url + api_version + 'token/refresh/',
        TokenRefreshView.as_view(),
        name='JWT_refresch',
    ),
    # swagger
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('swagger/',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger-ui'
    ),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # silk
    path('silk/', include('silk.urls', namespace='silk')),
    # media, static
    re_path(r'^media/(?P<path>.*)$', serve,{'document_root': settings.MEDIA_ROOT}),
    # re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT}),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

