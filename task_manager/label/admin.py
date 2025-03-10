from django.contrib import admin
from task_manager.label.models import Label


admin.site.register(Label, admin.ModelAdmin)
