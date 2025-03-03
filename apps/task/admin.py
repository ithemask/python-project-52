from apps.task.models import Task
from django.contrib import admin


admin.site.register(Task, admin.ModelAdmin)
