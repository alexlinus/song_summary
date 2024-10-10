from django.db import models


class SongStatuses(models.TextChoices):
    """Song statuses."""

    NEW = "new", "New"
    PROCESSED = "processed", "Processed"
    FAILED = "failed", "Failed"


class SongManager(models.Manager["SponsoredPage"]):

    def mark_unsuccessful(self, song_obj: "Song", message: str) -> None:
        song_obj.message = message
        song_obj.status = SongStatuses.FAILED
        song_obj.save(update_fields=["message", "status", "updated_at"])

    def mark_processed(self, song_obj: "Song", summary: str, countries: str) -> None:
        song_obj.summary = summary
        song_obj.countries = countries
        song_obj.status = SongStatuses.PROCESSED
        song_obj.save(update_fields=["summary", "countries", "status", "updated_at"])


class Song(models.Model):
    """Model to store song data."""
    # note it may be normalized in case of other requirements and further actions
    # (artist, title and countries may be moved) to a separate tables (or just artist and countries)
    artist = models.CharField(max_length=100)
    title = models.CharField(max_length=100)

    # summary of the song's lyrics in 1 sentence (e.g. “This song is about love and growing up..”)
    summary = models.TextField(blank=True, default="")

    countries = models.TextField(blank=True, default="")

    status = models.CharField(max_length=20, choices=SongStatuses.choices, default=SongStatuses.NEW)

    result_message = models.TextField(blank=True, default="", max_length=200)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = SongManager()

    class Meta:
        db_table = "songs"
        # note: we can think here over adding unique_together
        # in order not to create 2 records for the same artist and title
        ordering = ("-created_at",)

    def __str__(self):
        return f"{self.artist} - {self.title}"