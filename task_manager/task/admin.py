from django.contrib import admin
from task_manager.task.models import Task


admin.site.register(Task, admin.ModelAdmin)
