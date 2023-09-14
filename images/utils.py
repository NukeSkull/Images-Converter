import os
from django.conf import settings


def check_and_create_dir(dir_name):
    # Ensure the media and directories exist
    directory = os.path.join(settings.MEDIA_ROOT, dir_name)
    os.makedirs(directory, exist_ok=True)
    relative_path = os.path.relpath(directory)
    return relative_path
