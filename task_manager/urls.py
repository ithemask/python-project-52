from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path(
        'admin/',
        admin.site.urls,
    ),
    path(
        '',
        include('task_manager.core.urls'),
    ),
    path(
        'users/',
        include('task_manager.user.urls'),
    ),
    path(
        'statuses/',
        include('task_manager.status.urls'),
    ),
    path(
        'labels/',
        include('task_manager.label.urls'),
    ),
    path(
        'tasks/',
        include('task_manager.task.urls'),
    ),
]

handler400 = 'task_manager.core.views.bad_request_view'
handler403 = 'task_manager.core.views.permission_denied_view'
handler404 = 'task_manager.core.views.page_not_found_view'
handler500 = 'task_manager.core.views.server_error_view'
