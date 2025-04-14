from django.urls import path
from .views import FileUploadView, FileListView, FileDownloadView, FileDeleteView, file_detail_update, file_detail_page, file_list_page

urlpatterns = [
    path("", file_list_page, name="file-list-page"),
    path("api/upload/", FileUploadView.as_view(), name="file-upload"),
    path("api/files/", FileListView.as_view(), name="file-list"),
    path("api/download/<uuid:shareable_link>/", FileDownloadView.as_view(), name="file-download"),
    path("api/delete/<str:shareable_link>/", FileDeleteView.as_view(), name="file-delete"),
    path("api/file/<uuid:shareable_link>/", file_detail_update, name="file_detail_update"),
    path("file/<uuid:shareable_link>/", file_detail_page, name="file_detail_page"),
    ]
