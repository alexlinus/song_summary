"""Module contains implementations to work with MusxMatch."""
from http import HTTPStatus
import requests
from django.conf import settings

from apps.summarizer.utils import Result
from apps.summarizer.utils.cache import MusixMatchCacheKey

messages_by_status_codes = {
    HTTPStatus.BAD_REQUEST: "MusixMatch. The request had bad syntax or was inherently impossible to satisfy.",  # 400
    HTTPStatus.UNAUTHORIZED: "MusixMatch. Authentication failed, possibly due to invalid or missing API key.",  # 401
    HTTPStatus.PAYMENT_REQUIRED: "MusixMatch. The usage limit has been reached, or your balance is insufficient.",  # 402
    HTTPStatus.FORBIDDEN: "MusixMatch. You are not authorized to perform this operation.",  # 403
    HTTPStatus.NOT_FOUND: "MusixMatch. The requested resource was not found.",  # 404
    HTTPStatus.METHOD_NOT_ALLOWED: "MusixMatch. The requested method was not found.",  # 405
    HTTPStatus.INTERNAL_SERVER_ERROR: "MusixMatch. Oops. Something went wrong.",  # 500
    HTTPStatus.SERVICE_UNAVAILABLE: "MusixMatch is a bit busy at the moment and request can’t be satisfied.",  # 503
}


def _build_url(artist: str, title: str) -> str:
    query_string = f"?q_artist={artist}&q_track={title}&apikey={settings.MUSIX_MATCH_API_KEY}"
    return f"{settings.MUSIX_MATCH_BASE_API_URL}{query_string}"


def _extract_status_code_from_response(data: dict) -> int:
    return data["message"]["header"]["status_code"]


def get_lyrics(artist: str, title: str) -> tuple[str, Result]:
    result = Result()

    cache_key = MusixMatchCacheKey(key_postfix=hash(f"{artist}{title}"))
    if cached_data := cache_key.get_cache():
        return cached_data, result

    url = _build_url(artist=artist, title=title)

    try:
        response = requests.get(url)
    except Exception as exc:
        result.add_error(messages_by_status_codes[HTTPStatus.INTERNAL_SERVER_ERROR])
        return "", result

    if response.status_code != HTTPStatus.OK:
        result.add_error(messages_by_status_codes.get(response.status_code, "Musixmatch. Unknown error"))
        return "", result

    data = response.json()
    musix_match_status_code = _extract_status_code_from_response(data=data)
    if musix_match_status_code != HTTPStatus.OK:
        result.add_error(messages_by_status_codes.get(musix_match_status_code, "Musixmatch. Unknown error"))
        return "", result

    lyrics = data["message"]["body"]["lyrics"]["lyrics_body"]
    cache_key.set_cache(lyrics)
    return lyrics, result
