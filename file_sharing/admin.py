from django.contrib import admin
from .models import SharedFile

@admin.register(SharedFile)
class SharedFileAdmin(admin.ModelAdmin):
    list_display = ("id", "file", "uploaded_at", "shareable_link")  # Display key fields
    search_fields = ("file",)  # Enable search by filename
    list_filter = ("uploaded_at",)  # Filter files by date
    ordering = ("-uploaded_at",)  # Show newest files first
    readonly_fields = ("shareable_link",)  # Prevent editing the shareable link manually
