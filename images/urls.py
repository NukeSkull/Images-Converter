from django.urls import path
from images import views

urlpatterns = [
    path("images/", views.ImageConverterAPIView.as_view(), name="image-converter"),
    path("download/<int:image_id>/", views.download_image, name="download-image"),
    path("tasks/", views.TaskListView.as_view(), name="task-list"),
]
