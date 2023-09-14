from .base import *

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

import os

MIDDLEWARE += [
    "corsheaders.middleware.CorsMiddleware",
]

CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql_psycopg2",
        "NAME": "images_converter",
        "USER": "postgres",
        "PASSWORD": "postgres",
        "HOST": os.getenv("DATABASE_HOST"),
        "PORT": os.getenv("DATABASE_PORT"),
    }
}
