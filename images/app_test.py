import os
import shutil
import json
import pytest

from django.conf import settings
from PIL import Image, ImageDraw
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from .models import Image as MyImage
from .models import Task
from images.tasks import convert_image_task
from images.utils import check_and_create_dir

PNG_PATH = os.path.join(settings.MEDIA_ROOT, settings.PNG_DIR, "test_image.png")
JPG_PATH = os.path.join(settings.MEDIA_ROOT, settings.JPG_DIR, "test_image.jpg")
TEST_PATH = os.path.join(settings.MEDIA_ROOT, settings.TEST_DIR, "test_image.png")

# Create your tests here.


@pytest.fixture
def client():
    return APIClient()


@pytest.fixture
def fixture_create_processed_images():
    # Create two Image objects
    image1 = MyImage.objects.create(
        png_image=os.path.join(settings.PNG_DIR, "sonic_test.png"),
        jpg_image=os.path.join(settings.JPG_DIR, "sonic_test.jpg"),
        name="sonic_test.png",
        size=233293,
    )
    image2 = MyImage.objects.create(
        png_image=os.path.join(settings.PNG_DIR, "mario_test.png"),
        jpg_image=os.path.join(settings.JPG_DIR, "mario_test.jpg"),
        name="mario_test.png",
        size=2256116,
    )

    # Create two Task objects associated with the Image objects
    task1 = Task.objects.create(
        task_id="b4c9e559-9f8c-4de4-98e3-d79a3fddfbcd", status="SUCCESS", image=image1
    )
    task2 = Task.objects.create(
        task_id="f027dd92-d120-42e3-a947-25666e938868", status="SUCCESS", image=image2
    )

    return [image1, image2]


# Create test image in TEST directory. For tests that need an image from outside the app
@pytest.fixture(scope="module")
def fixture_create_test_image():
    # Generate test image and save it into TEST dir
    test_dir = check_and_create_dir(settings.TEST_DIR)
    image_path = create_image(test_dir)
    yield image_path

    shutil.rmtree(os.path.join(settings.BASE_DIR, test_dir))


# Create test image in PNG directory. For tests that need an image already in the app
@pytest.fixture
def fixture_create_test_image_no_jpg_save_ddbb():
    # Generate test image and save it into PNG dir
    png_dir = check_and_create_dir(settings.PNG_DIR)
    test_image_path = create_image(png_dir)

    yield MyImage.objects.create(
        png_image=os.path.join(settings.PNG_DIR, "test_image.png"),
        name="test_image.png",
        size=233293,
    )
    # Remove generated png image from disk
    os.remove(os.path.join(os.getcwd(), png_dir, test_image_path))


# Assert response status code, that the number of images in database are the same as
# the number of images at response and that each image in response has a name and status
@pytest.mark.django_db
def test_image_converter_api_view_get(client, fixture_create_processed_images):
    # Get the number of Image objects in database
    num_images = MyImage.objects.count()

    # Make GET request to /converter endpoint
    response = client.get(reverse("image-converter"))
    # Assert that response contains the correct number of objects,
    # each with an image_name and status field
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) == num_images
    assert all("image_name" in obj and "status" in obj for obj in response.data)

    # Assert that the response data matches the expected data from the fixture
    images = fixture_create_processed_images
    for i in range(num_images):
        image = images[i]
        expected_data = {
            "id": image.id,
            "png_image": image.png_image.url,
            "image_name": image.name,
            "status": image.tasks.first().status if image.tasks.exists() else None,
        }

        # Convert the response data to a regular dictionary
        response_data = json.loads(json.dumps(response.data[i]))

        assert response_data == expected_data


# Assert status code, image returned is the test image, last task generated is the one
# in response, assert both png anf jpg image exist in disk and delete them
@pytest.mark.django_db
def test_image_converter_api_view_post_create(client, fixture_create_test_image):
    try:
        full_path = os.path.join(settings.BASE_DIR, TEST_PATH)
        test_image = open(full_path, "rb")
        data = {"png_image": test_image}

        # Make POST request to /converter endpoint with test image data
        response = client.post(reverse("image-converter"), data, format="multipart")
        # Assert that response contains the correct data
        assert response.status_code == status.HTTP_201_CREATED
        assert (
            "image_name" in response.data
            and response.data["image_name"] == fixture_create_test_image
        )

        # Assert both png image and jpg_image exists in disk and delete them
        assert os.path.exists(PNG_PATH)
        assert os.path.exists(JPG_PATH)
    finally:
        clean_disk()


# assert that when uploading an already existing image it overrides it
@pytest.mark.django_db
def test_image_converter_api_view_post_override(client, fixture_create_test_image):
    try:
        full_path = os.path.join(os.getcwd(), TEST_PATH)
        test_image = open(full_path, "rb")
        data = {"png_image": test_image}

        client.post(reverse("image-converter"), data, format="multipart")

        # Reopen image before the second post
        test_image = open(full_path, "rb")
        data = {"png_image": test_image}

        response = client.post(reverse("image-converter"), data, format="multipart")

        assert response.status_code == status.HTTP_201_CREATED
        assert response.data["status"] == "SUCCESS"
        assert (
            "image_name" in response.data
            and response.data["image_name"] == fixture_create_test_image
        )

    finally:
        # Delete both png and jpg images generated during the test
        clean_disk()


# assert that the image send has a jpg_image and assert that the jpg image is saved on
# disk, then delete it
@pytest.mark.django_db
def test_convert_image_task(fixture_create_test_image_no_jpg_save_ddbb):
    try:
        # Call Celery task
        convert_image_task.delay(fixture_create_test_image_no_jpg_save_ddbb.id)

        # Retrieve the updated image from the database
        fixture_create_test_image_no_jpg_save_ddbb.refresh_from_db()

        # Assert that the task has successfully converted the image
        assert fixture_create_test_image_no_jpg_save_ddbb.jpg_image is not None
        assert fixture_create_test_image_no_jpg_save_ddbb.jpg_image != ""

        # Assert jpg image exists
        assert os.path.exists(JPG_PATH)

    finally:
        # Remove generated jpg image from disk if exists
        if os.path.exists(JPG_PATH):
            os.remove(JPG_PATH)


# Assert the status code, that the content is a jpg, check that the image name matches
# the image requested and assert that response content is equal to the image file
@pytest.mark.django_db
def test_download_image(client, fixture_create_test_image):
    try:
        full_path = os.path.join(settings.BASE_DIR, TEST_PATH)
        test_image = open(full_path, "rb")
        data = {"png_image": test_image}

        # Make POST request to /converter endpoint with test image data
        response = client.post(reverse("image-converter"), data, format="multipart")
        image = MyImage.objects.get(name=response.data["image_name"])

        # Make GET request to download_image endpoint with test image ID
        response = client.get(reverse("download-image", kwargs={"image_id": image.id}))

        # Assert that response contains the expected content type and filename
        assert response.status_code == status.HTTP_200_OK
        assert response.get("Content-Type") == "image/jpeg"
        assert (
            response.get("Content-Disposition")
            == f'attachment; filename="{image.name.replace(".png", ".jpg")}"'
        )

        # Assert that response content is equal to the image file content
        content = b"".join(response.streaming_content)
        assert content == image.jpg_image.read()

    finally:
        # Delete both png and jpg images generated during the test
        clean_disk()


def create_image(destination):
    img = Image.new("RGBA", (100, 100), (255, 0, 0, 0))

    draw = ImageDraw.Draw(img)
    draw.ellipse((25, 25, 75, 75), fill=(255, 0, 0))

    test_image_path = "test_image.png"
    img.save(os.path.join(destination, test_image_path), "PNG")

    return test_image_path


def clean_disk():
    os.remove(os.path.join(settings.BASE_DIR, PNG_PATH))
    os.remove(os.path.join(settings.BASE_DIR, JPG_PATH))
