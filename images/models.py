from django.db import models

# Create your models here.


class Image(models.Model):
    png_image = models.ImageField(upload_to="PNGs/")
    jpg_image = models.ImageField(upload_to="JPGs/", null=True, blank=True)
    name = models.CharField(max_length=255, unique=True)
    size = models.IntegerField()
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    task_id = models.CharField(max_length=255, primary_key=True)
    status = models.CharField(max_length=255)
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)
    image = models.ForeignKey(
        Image, on_delete=models.CASCADE, to_field="name", related_name="tasks"
    )

    def __str__(self):
        return self.task_id
