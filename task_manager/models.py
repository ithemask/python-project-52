from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import ProtectedError
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    first_name = models.CharField(
        _('first name'),
        max_length=150,
    )
    last_name = models.CharField(
        _('last name'),
        max_length=150,
    )

    def __str__(self):
        return self.get_full_name()


class Status(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.name


class Label(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    def __str__(self):
        return self.name

    def delete(self, *args, **kwargs):
        if self.tasks.exists():
            raise ProtectedError('', self)
        super().delete(*args, **kwargs)


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
