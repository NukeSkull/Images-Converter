FROM python:3.7-alpine AS base

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTHECODE=1

WORKDIR /sp-tools-images-converter/

COPY requirements/* ./requirements/

RUN apk add -u zlib-dev jpeg-dev gcc musl-dev
RUN python3 -m pip install --upgrade pip

RUN apk add --virtual .build-deps --no-cache postgresql-dev gcc python3-dev musl-dev && \
        pip install --no-cache-dir -r requirements/test.txt && \
        apk --purge del .build-deps

COPY ./images ./images
COPY ./images_converter ./images_converter
COPY ./manage.py ./pytest.ini ./.env ./

FROM base AS django

EXPOSE 8000

COPY ./docker/entrypoint.sh ./

ENTRYPOINT /sp-tools-images-converter/entrypoint.sh

FROM base AS celery_workers

CMD [ "celery", "-A", "images_converter", "worker", "-l", "INFO", "--hostname=rabbitmq" ]
