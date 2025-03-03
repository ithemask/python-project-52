from apps.core import views
from django.urls import path


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