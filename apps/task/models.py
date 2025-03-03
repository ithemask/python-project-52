from apps.label.models import Label
from apps.status.models import Status
from apps.user.models import User
from django.db import models


class Task(models.Model):
    name = models.CharField(
        max_length=100,
        unique=True,
    )
    description = models.TextField(
        null=True,
        blank=True,
    )
    status = models.ForeignKey(
        Status,
        on_delete=models.PROTECT,
    )
    author = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='author_tasks',
        null=True,
        blank=True,
    )
    executor = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='executor_tasks',
        null=True,
        blank=True,
    )
    labels = models.ManyToManyField(
        Label,
        related_name='tasks',
        blank=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.name
