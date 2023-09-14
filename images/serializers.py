import os
import uuid

from celery.states import PENDING
from django.conf import settings
from django.utils import timezone
from rest_framework import serializers

from .models import Image, Task
from .tasks import convert_image_task
from .utils import check_and_create_dir


class ImageSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    png_image = serializers.ImageField(required=True)
    image_name = serializers.CharField(source="name", read_only=True)
    status = serializers.SerializerMethodField()

    def get_status(self, obj):
        latest_task = obj.tasks.all().order_by("-started_at").first()
        return latest_task.status if latest_task else None

    def create(self, validated_data):
        png_image = validated_data["png_image"]

        img, created = Image.objects.get_or_create(
            name=png_image.name,
            defaults={
                "png_image": png_image,
                "name": png_image.name,
                "size": png_image.size,
            },
        )
        if not created:
            # Delete current image and override with new one
            override_image(img, png_image)

        handle_uploaded_image(png_image, img.id)

        return img


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ("task_id", "status", "started_at", "ended_at", "image")


def override_image(old_image, new_image):
    png_path = old_image.png_image

    os.remove(os.path.join(settings.MEDIA_ROOT, str(old_image.png_image)))
    os.remove(os.path.join(settings.MEDIA_ROOT, str(old_image.jpg_image)))

    Image.objects.filter(name=old_image.name).update(
        png_image=png_path,
        jpg_image=None,
        size=new_image.size,
        uploaded_at=timezone.now(),
    )


def handle_uploaded_image(form_image, image_id):
    pngs_dir = check_and_create_dir(settings.PNG_DIR)
    image = Image.objects.get(id=image_id)

    with open(os.path.join(pngs_dir, image.name), "wb+") as destination:
        for chunk in form_image.chunks():
            destination.write(chunk)

    image_task = Image.objects.get(name=image.name)

    # Generate task ID and save it into ddbb
    task_id = str(uuid.uuid4())
    Task.objects.create(task_id=task_id, image=image_task, status=PENDING)

    # Initiate task with generated ID
    convert_task = convert_image_task.apply_async(
        kwargs={"image_id": image.id}, task_id=task_id
    )
