import os

from django.conf import settings
from PIL import Image
from .models import Image
from .models import Task
from rest_framework.views import APIView
from django.http import FileResponse
from rest_framework.decorators import api_view
from rest_framework import status, generics
from rest_framework.response import Response
from .serializers import ImageSerializer, TaskSerializer


# Create your views here.
class ImageConverterAPIView(APIView):
    serializer_class = ImageSerializer

    def get(self, request, format=None):
        images = Image.objects.all()
        serialized_data = self.serializer_class(images, many=True).data
        return Response(serialized_data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid(raise_exception=True):
            image = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


def populate_relations_dic(images):
    relations = {}

    for image in images:
        # Get all tasks related to task image and sort them by started_at
        sorted_tasks = image.tasks.all().order_by("-started_at")
        # Keep the status of the most recent task
        relations[image.id] = {"name": image.name, "status": sorted_tasks[0].status}
    return relations


@api_view(["GET"])
def download_image(request, image_id):
    image = Image.objects.get(id=image_id)
    image_path = os.path.join(settings.MEDIA_ROOT, str(image.jpg_image))
    response = FileResponse(open(image_path, "rb"), content_type="image/jpeg")
    response["Content-Disposition"] = 'attachment; filename="{0}"'.format(
        image.name.replace(".png", ".jpg")
    )
    return response


class TaskListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    queryset = Task.objects.all()
