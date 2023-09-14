from .base import *

import os

CELERY_TASK_ALWAYS_EAGER = True

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "test_ImagesConverter",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": os.getenv("DATABASE_HOST"),
        "PORT": os.getenv("DATABASE_PORT"),
    }
}

TEST_DIR = "TEST/"
