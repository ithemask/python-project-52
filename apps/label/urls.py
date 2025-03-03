from apps.label import views
from django.urls import path


urlpatterns = [
    path(
        '',
        views.LabelListView.as_view(),
        name='label-list',
    ),
    path(
        'create/',
        views.LabelCreateView.as_view(),
        name='label-create',
    ),
    path(
        '<int:pk>/update/',
        views.LabelUpdateView.as_view(),
        name='label-update',
    ),
    path(
        '<int:pk>/delete/',
        views.LabelDeleteView.as_view(),
        name='label-delete',
    ),
]
