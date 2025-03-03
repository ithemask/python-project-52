from apps.user import views
from django.urls import path


urlpatterns = [
    path(
        '',
        views.UserListView.as_view(),
        name='user-list',
    ),
    path(
        'create/',
        views.UserCreateView.as_view(),
        name='user-create',
    ),
    path(
        '<int:pk>/update/',
        views.UserUpdateView.as_view(),
        name='user-update',
    ),
    path(
        '<int:pk>/delete/',
        views.UserDeleteView.as_view(),
        name='user-delete',
    ),
]
