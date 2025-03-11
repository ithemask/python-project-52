from django.conf import settings
from django.urls import include, path

from task_manager.core import views

urlpatterns = [
    path(
        '',
        views.IndexView.as_view(),
        name='index',
    ),
    path(
        'login/',
        views.UserLoginView.as_view(),
        name='login',
    ),
    path(
        'logout/',
        views.UserLogoutView.as_view(),
        name='logout',
    ),
]


if settings.IS_TESTING:
    urlpatterns += [
        path('', include('task_manager.core.error_test_urls')),
    ]
