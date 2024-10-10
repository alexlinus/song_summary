# Register your models here.
from django.contrib import admin
from .models import Song
from .models.song import SongStatuses
from .tasks import process_song


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ["artist", "title", "summary", "countries", "status", "result_message", "created_at", "updated_at"]
    list_filter = ["status", "created_at", "updated_at"]
    search_fields = ["artist", "title", "summary", "countries"]
    ordering = ["-updated_at"]

    read_only_fields = ["result_message", "created_at", "updated_at", "status", "summary", "countries"]

    def get_readonly_fields(self, request, obj=None):
        if not obj:
            return self.read_only_fields
        return self.read_only_fields + ["artist", "title"]

    def save_model(self, request, obj, form, change):
        response = super().save_model(request, obj, form, change)
        if obj.status != SongStatuses.PROCESSED:
            # call song processing
            process_song.delay(obj.pk)
        return response
