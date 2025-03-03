from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path(
        'admin/',
        admin.site.urls,
    ),
    path(
        '',
        include('apps.core.urls'),
    ),
    path(
        'users/',
        include('apps.user.urls'),
    ),
    path(
        'statuses/',
        include('apps.status.urls'),
    ),
    path(
        'labels/',
        include('apps.label.urls'),
    ),
    path(
        'tasks/',
        include('apps.task.urls'),
    ),
]
