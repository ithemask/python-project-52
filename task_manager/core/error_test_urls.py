from django.urls import path
from task_manager.core import error_test_views


urlpatterns = [
    path(
        'bad-request/',
        error_test_views.trigger_400_view,
    ),
    path(
        'forbidden/',
        error_test_views.trigger_403_view,
    ),
    path(
        'causes-500/',
        error_test_views.trigger_500_view,
    ),
]
