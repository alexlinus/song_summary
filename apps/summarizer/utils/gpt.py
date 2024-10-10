"""Module contains implementations to work with OpenAI."""

from functools import partial

import openai
from django.conf import settings

from apps.summarizer.utils import Result
from apps.summarizer.utils.cache import MusixMatchCacheKey

client = openai.OpenAI(
    api_key=settings.OPEN_AI_API_KEY,
)


class OpenAIClient:
    """Just a wrapper of openAI client, to send requests."""
    completion_create = partial(
        client.chat.completions.create,
        model=settings.GPT_MODEL,
    )

    @classmethod
    def send_request(cls, prompt: str) -> tuple[str, Result]:
        result = Result()
        cache_key = MusixMatchCacheKey(key_postfix=hash(prompt))

        if cached_data := cache_key.get_cache():
            return cached_data, result

        try:
            response = cls.completion_create(messages=[{"role": "user", "content": prompt}])
        except openai.APIConnectionError:
            result.add_error("OpenAI: Failed to connect to the OpenAI API. Try a bit later.")
            return "", result
        except openai.RateLimitError:
            result.add_error("OpenAI: We were limited by rate limiter")
            return "", result
        except openai.APIStatusError as exc:
            result.add_error("OpenAI: API doesn't respond!")
            return "", result
        except Exception:
            result.add_error("OpenAI: Something went wrong!")
            return "", result
        else:
            gpt_content = response.choices[0].message.content.strip()
            cache_key.set_cache(gpt_content)
            return gpt_content, result


def summarize_lyrics(lyrics: str) -> tuple[str, Result]:
    """Send request to OpenAI to get song summary."""
    prompt = settings.GPT_SUMMARIZE_LYRICS_PROMPT.format(lyrics=lyrics)
    response, result = OpenAIClient.send_request(prompt=prompt)
    return response, result


def extract_countries(lyrics) -> tuple[str, Result]:
    """Send request to OpenAI to extract countries from our song."""
    prompt = settings.GPT_EXTRACT_COUNTRIES_PROMPT.format(lyrics=lyrics)
    response, result = OpenAIClient.send_request(prompt=prompt)
    return response, result
