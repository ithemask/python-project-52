from django.contrib import admin
from django.urls import path
from task_manager import views


urlpatterns = [
    path(
        'admin/',
        admin.site.urls,
    ),
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
        'users/',
        views.UserListView.as_view(),
        name='user-list',
    ),
    path(
        'users/create/',
        views.UserCreateView.as_view(),
        name='user-create',
    ),
    path(
        'users/<int:pk>/update/',
        views.UserUpdateView.as_view(),
        name='user-update',
    ),
    path(
        'users/<int:pk>/delete/',
        views.UserDeleteView.as_view(),
        name='user-delete',
    ),
    path(
        'statuses/',
        views.TemplateView.as_view(),
        name='status-list',
    ),
    path(
        'labels/',
        views.TemplateView.as_view(),
        name='label-list',
    ),
    path(
        'tasks/',
        views.TemplateView.as_view(),
        name='task-list',
    ),
]
