from typing import Any

import redis


class RedisService:
    def __init__(self, host: str, port: int = 6379):
        """Initialize the Redis client"""
        self.redis_client = redis.Redis(host=host, port=port)

    def save_media_with_metadata(
            self,
            media_id: str,
            media_data: bytes,
            metadata: dict,
            expire: int = 86400
    ):
        """
        Save media with metadata in redis with expire time

        Args:
            media_id: a unique identifier for the media
            media_data: the media data in bytes
            metadata: a dictionary of metadata for the media
            expire: the expire time in seconds
        """
        self.redis_client.hset(f'media:metadata:{media_id}', mapping=metadata)
        self.redis_client.set(f'media:data:{media_id}', media_data, expire)
        self.redis_client.expire(f'media:data:{media_id}', expire)

    def get_media_with_metadata(self, media_id: str) -> dict[str, Any]:
        """
        Get media with metadata from redis

        Args:
            media_id: a unique identifier for the media
        """
        metadata: dict = self.redis_client.hgetall(f'media:metadata:{media_id}')
        media_data: bytes = self.redis_client.get(f'media:data:{media_id}')

        result = {
            "chat": metadata.get("chat"),
            "media_type": metadata.get("media_type"),
            "file_bytes": media_data
        }

        return result

    def close(self):
        self.redis_client.close()