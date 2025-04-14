from django.db import models
import uuid

class SharedFile(models.Model):
    file = models.FileField(upload_to="uploads/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    shareable_link = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def __str__(self):
        return self.file.name
