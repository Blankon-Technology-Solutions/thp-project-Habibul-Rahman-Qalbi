from .default import *  # noqa

REDIS_IP = "redis"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_IP}:6379/1",
    },
}
