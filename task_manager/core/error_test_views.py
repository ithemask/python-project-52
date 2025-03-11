from django.core.exceptions import PermissionDenied, SuspiciousOperation


def trigger_400_view(request):
    raise SuspiciousOperation()


def trigger_403_view(request):
    raise PermissionDenied()


def trigger_500_view(request):
    raise Exception()
