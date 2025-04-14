from rest_framework import generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.http import FileResponse
from .models import SharedFile
from .serializers import SharedFileSerializer,ShareFileSerializer
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.core.files.storage import default_storage
from rest_framework.decorators import api_view
from uuid import UUID


@method_decorator(csrf_exempt, name="dispatch")
class FileUploadView(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, *args, **kwargs):
        file_serializer = SharedFileSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()
            return Response({
                "message": "File uploaded successfully",
                "download_link": f"/api/download/{file_serializer.data['shareable_link']}/"
            })
        return Response(file_serializer.errors, status=400)

class FileListView(generics.ListAPIView):
    queryset = SharedFile.objects.all()
    serializer_class = SharedFileSerializer

class FileDownloadView(APIView):
    def get(self, request, shareable_link, *args, **kwargs):
        file_obj = get_object_or_404(SharedFile, shareable_link=shareable_link)
        return FileResponse(open(file_obj.file.path, "rb"), as_attachment=True)

class FileDeleteView(APIView):
    def delete(self, request, shareable_link, *args, **kwargs):
        try:
            shareable_link = UUID(shareable_link)  # Convert manually
        except ValueError:
            return Response({"error": "Invalid UUID format"}, status=400)

        file_obj = get_object_or_404(SharedFile, shareable_link=shareable_link)
        file_obj.delete()
        return Response({"message": "File deleted successfully"})



@api_view(["GET", "PUT"])
def file_detail_update(request, shareable_link):
    """
    Retrieve or update a file using the unique shareable link.
    """
    shared_file = get_object_or_404(SharedFile, shareable_link=shareable_link)

    if request.method == "GET":
        serializer = ShareFileSerializer(shared_file, context={"request": request})  # Pass request context
        return Response(serializer.data)

    elif request.method == "PUT":
        if shared_file.file:
            default_storage.delete(shared_file.file.name)

        shared_file.file = request.FILES.get("file")
        shared_file.save()

        file_url = request.build_absolute_uri(shared_file.file.url)  # Get full URL
        return JsonResponse({"message": "File updated successfully", "file_url": file_url})


def file_detail_page(request, shareable_link):
    """
    Serve the file detail page for a given shareable link.
    """
    return render(request, "file_detail.html", {"shareable_link": shareable_link})

def file_list_page(request):
    """
    Fetch the list of files from the SharedFile model and display them in a template.
    """
    files = SharedFile.objects.all()  # Get all files from the SharedFile model

    return render(request, "index.html", {"files": files})