"""Module contains implementations to work with cache."""
from typing import Any

from django.conf import settings
from django.core.cache import cache


class BaseCacheKey(str):
    """String implementation for cache keys."""

    __slots__ = ()

    key_pattern: str
    timeout = 60 * 60 * 24  # one day

    def __new__(cls, *args, **kwargs):
        key = cls.key_pattern.format(*args, **kwargs)
        return super().__new__(cls, key)

    def get_cache(self) -> Any:
        return cache.get(str(self))

    def set_cache(self, value: str) -> None:
        cache.set(str(self), value, timeout=self.timeout)


class MusixMatchCacheKey(BaseCacheKey):
    timeout = settings.MUSIX_MATCH_CACHE_TIMEOUT_SECONDS
    key_pattern = "MMK:{key_postfix}"


class OpenAICacheKey(BaseCacheKey):
    timeout = settings.OPEN_AI_CACHE_TIMEOUT_SECONDS
    key_pattern = "OAK:{key_postfix}}"
