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

handler400 = 'apps.core.views.bad_request_view'
handler403 = 'apps.core.views.permission_denied_view'
handler404 = 'apps.core.views.page_not_found_view'
handler500 = 'apps.core.views.server_error_view'
