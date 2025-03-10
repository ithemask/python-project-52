from django.urls import path
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
    path(
        'bad-request/',
        views.trigger_400_view,
    ),
    path(
        'forbidden/',
        views.trigger_403_view,
    ),
    path(
        'causes-500/',
        views.trigger_500_view,
    ),
]
