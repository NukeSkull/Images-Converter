from django.contrib import admin
from .models import Image
from .models import Task

# Register your models here.


class ImageAdmin(admin.ModelAdmin):
    list_display = ("png_image", "jpg_image", "name", "size", "uploaded_at")


class TaskAdmin(admin.ModelAdmin):
    list_display = ("task_id", "image", "status", "started_at", "ended_at")


admin.site.register(Image, ImageAdmin)
admin.site.register(Task, TaskAdmin)
