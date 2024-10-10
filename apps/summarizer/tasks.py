from celery import shared_task

from apps.summarizer.models import Song
from apps.summarizer.utils.musixmatch import get_lyrics
from apps.summarizer.utils.gpt import summarize_lyrics, extract_countries


@shared_task
def process_song(song_id: int) -> None:
    """Celery task to process song."""

    try:
        song_obj = Song.objects.get(pk=song_id)
    except Song.DoesNotExist:
        return

    lyrics, result = get_lyrics(title=song_obj.title, artist=song_obj.artist)
    if not result.is_successful:
        Song.objects.mark_unsuccessful(song_obj=song_obj, result=result.message)
        return

    song_summary, result = summarize_lyrics(lyrics=lyrics)
    if not result.is_successful:
        Song.objects.mark_unsuccessful(song_obj=song_obj, result=result.message)
        return

    list_of_countries, result = extract_countries(lyrics=lyrics)
    if not result.is_successful:
        Song.objects.mark_unsuccessful(song_obj=song_obj, result=result.message)
        return

    Song.objects.mark_processed(song_obj=song_obj, summary=song_summary, countries=list_of_countries)
