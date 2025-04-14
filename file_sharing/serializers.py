from rest_framework import serializers
from .models import SharedFile
from django.conf import settings

class SharedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SharedFile
        fields = ["id", "file", "uploaded_at", "shareable_link"]

class ShareFileSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField()

    class Meta:
        model = SharedFile
        fields = ["id", "file", "file_url", "uploaded_at", "shareable_link"]

    def get_file_url(self, obj):
        request = self.context.get("request")
        if request is not None:
            return request.build_absolute_uri(obj.file.url)
        return f"{settings.MEDIA_URL}{obj.file.url}"