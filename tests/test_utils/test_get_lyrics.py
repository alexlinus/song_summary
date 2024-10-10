import pytest
from unittest.mock import Mock, patch
from apps.summarizer.utils import Result

from apps.summarizer.utils.musixmatch import get_lyrics


@pytest.fixture
def mock_requests_get():
    with patch('requests.get') as mock_get:
        yield mock_get


@pytest.fixture
def mock_cache_key():
    with patch('apps.summarizer.utils.musixmatch.MusixMatchCacheKey') as mock_key:
        yield mock_key


@pytest.mark.django_db
def test_get_lyrics_cached(mock_cache_key):
    # Given: mocked cached key to return cached value
    cache_key_instance = mock_cache_key.return_value
    cache_key_instance.get_cache.return_value = 'cached_lyrics'
    # When: we call .get_lyrics()
    lyrics, result = get_lyrics('Queen', 'Bohemian Rhapsody')

    # Then: we should receive cached lyrics
    assert lyrics == 'cached_lyrics'
    assert isinstance(result, Result)

    # Then: result should be successful
    assert result.message == ""
    assert result.is_successful


@pytest.mark.django_db
def test_get_lyrics_ok_response(mock_requests_get, mock_cache_key):
    # Given: mocked cache  with empty value
    # mocked response status code as successful
    # mocked body with success internal status code
    cache_key_instance = mock_cache_key.return_value
    cache_key_instance.get_cache.return_value = None
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        'message': {'header': {'status_code': 200}, 'body': {'lyrics': {'lyrics_body': 'Queen Lyrics'}}}}
    mock_requests_get.return_value = response

    # When: we call .get_lyrics()
    lyrics, result = get_lyrics('Queen', 'Bohemian Rhapsody')

    # Then: we should receive lyrics
    assert lyrics == 'Queen Lyrics'
    assert isinstance(result, Result)

    # Then: there shouldn't be any error message
    assert result.is_successful
    assert result.message == ""
    # Then: we should set cache after successful receiving from API.
    cache_key_instance.set_cache.assert_called_once_with('Queen Lyrics')


@pytest.mark.django_db
def test_get_lyrics_request_exception(mock_requests_get, mock_cache_key):
    # Given: empty cache
    # mocked request with some exception
    cache_key_instance = mock_cache_key.return_value
    cache_key_instance.get_cache.return_value = None
    mock_requests_get.side_effect = Exception()

    # When: we call get_lyrics()
    lyrics, result = get_lyrics('Queen', 'Bohemian Rhapsody')

    # Then: we should receive empty lyrics and result message should tell us what was wrong
    assert lyrics == ''
    assert isinstance(result, Result)
    assert result.message == 'MusixMatch. Oops. Something went wrong.'


@pytest.mark.django_db
def test_get_lyrics_non_ok_status(mock_requests_get, mock_cache_key):
    # Given: mocked empty cache value
    # mocked response with 403 status code to test we process it just in case
    cache_key_instance = mock_cache_key.return_value
    cache_key_instance.get_cache.return_value = None
    response = Mock()
    response.status_code = 403
    response.json.return_value = {'message': {'header': {'status_code': 200}, 'body': {'lyrics': {'lyrics_body': ''}}}}
    mock_requests_get.return_value = response

    # When: we call .get_lyrics()
    lyrics, result = get_lyrics('Queen', 'Bohemian Rhapsody')

    # Then: we should receive empty string and result message about what was wrong
    assert lyrics == ''
    assert isinstance(result, Result)
    assert not result.is_successful
    assert result.message == 'MusixMatch. You are not authorized to perform this operation.'


@pytest.mark.django_db
def test_get_lyrics_musixmatch_error_code(mock_requests_get, mock_cache_key):
    # Given: mocked cache with empty value
    # mocked http response with 200 status code
    # but internal status code in the body, we mocked as unsuccessful with 503 status cde
    cache_key_instance = mock_cache_key.return_value
    cache_key_instance.get_cache.return_value = None
    response = Mock()
    response.status_code = 200
    response.json.return_value = {'message': {'header': {'status_code': 503}, 'body': {'lyrics': {'lyrics_body': ''}}}}
    mock_requests_get.return_value = response

    # When: we call get_lyrics
    lyrics, result = get_lyrics('Queen', 'Bohemian Rhapsody')

    # Then: we should receive empty lyrics value
    # and error message about what was wrong.
    assert lyrics == ''
    assert isinstance(result, Result)
    assert not result.is_successful
    assert result.message == "MusixMatch is a bit busy at the moment and request can’t be satisfied."
