from django.db import models


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
            raise models.ProtectedError('', self)
        super().delete(*args, **kwargs)
