from __future__ import absolute_import, unicode_literals

from celery import shared_task
from .utils import check_and_create_dir
from PIL import Image
from .models import Image as ImageModel
from .models import Task
from celery.states import SUCCESS, FAILURE
from datetime import datetime
from django.conf import settings

import os


@shared_task
def convert_image_task(image_id):
    try:
        image = ImageModel.objects.get(id=image_id)

        jpgs_dir = check_and_create_dir(settings.JPG_DIR)

        img_path = os.path.join(settings.MEDIA_ROOT, settings.PNG_DIR, image.name)
        img = Image.open(img_path)
        # Create a new white image with the same size as the original image
        new_img = Image.new("RGB", img.size, (255, 255, 255))
        # Paste the original image onto the new white image
        new_img.paste(img, (0, 0), img)
        # Save the new image as a JPG
        image_name_jpg = image.name.replace(".png", ".jpg")
        image_path_jpg = os.path.join(jpgs_dir, image_name_jpg)
        new_img.save(image_path_jpg)

        # Update ddbb with new jpg image
        image.jpg_image = image_path_jpg.replace("media/", "")
        image.save()

        # Update task status before ending
        update_task(convert_image_task.request.id, SUCCESS)

    # Change task status to failure in case ant celery error occurs
    except Exception:
        update_task(convert_image_task.request.id, FAILURE)


def update_task(task_id, status):
    Task.objects.filter(task_id=task_id).update(status=status, ended_at=datetime.now())
