# app/services/cache.py

from __future__ import annotations

from typing import Any, Optional
import json
import os

from redis import Redis, ConnectionError  # type: ignore

# ✅ absolute import so editor + runtime are happy
from app.config import settings

# Prefer orjson if present (faster); fall back to stdlib json
try:
    import orjson  # type: ignore

    def json_dumps(v: Any) -> str:
        return orjson.dumps(v).decode("utf-8")

    def json_loads(s: str) -> Any:
        return orjson.loads(s)

except Exception:
    def json_dumps(v: Any) -> str:
        return json.dumps(v, ensure_ascii=False)

    def json_loads(s: str) -> Any:
        return json.loads(s)


_redis: Optional[Redis] = None


def get_client() -> Redis:
    """
    Lazy-create and return a singleton Redis client.
    Raises a clear error if Redis isn't reachable.
    """
    global _redis
    if _redis is None:
        _redis = Redis.from_url(settings.redis_url, decode_responses=True)
        # Light health check to fail fast with a helpful message.
        try:
            _redis.ping()
        except ConnectionError as e:
            raise RuntimeError(
                "Cannot connect to Redis. Is Docker running and the 'fba_redis' container up? "
                "Try:  docker compose up -d"
            ) from e
    return _redis


def cache_get(key: str) -> Any | None:
    """
    Get a JSON value by key. Returns None if not found or JSON is invalid.
    """
    r = get_client()
    raw = r.get(key)
    if raw is None:
        return None
    try:
        return json_loads(raw)
    except Exception:
        # If somehow non-JSON got stored, just return the raw string.
        return raw


def cache_set(key: str, value: Any, ttl_seconds: int = 300) -> None:
    """
    Set a JSON value with TTL (seconds).
    """
    r = get_client()
    r.setex(key, ttl_seconds, json_dumps(value))


def cache_delete(key: str) -> int:
    """
    Delete a key. Returns number of keys removed (0 or 1).
    """
    r = get_client()
    return r.delete(key)


def cache_ttl(key: str) -> int:
    """
    Return remaining TTL in seconds, or -1 if no TTL, or -2 if key doesn't exist.
    """
    r = get_client()
    return r.ttl(key)
