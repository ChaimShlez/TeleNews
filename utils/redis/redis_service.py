from typing import Any

import redis


class RedisService:
    def __init__(self, host: str, port: int = 6379):
        """Initialize the Redis client"""
        self.redis_client = redis.Redis(host=host, port=port)

    def save_media_with_metadata(
            self,
            media_id: str,
            title_id: str,
            media_type: str,
            media_data: bytes,
            expire: int = 86400
    ):
        """
        Save media with metadata in redis with expire time

        Args:
            media_id: a unique identifier for the media
            title_id: a unique identifier for the title
            media_type: the type of the media
            media_data: the media data in bytes
            expire: the expire time in seconds
        """
        hash_name = f'media:{media_id}:{title_id}'
        self.redis_client.hset(hash_name, "title_id", title_id)
        self.redis_client.hset(hash_name, "media_type", media_type)
        self.redis_client.hset(hash_name, "media_data", media_data)
        self.redis_client.expire(hash_name, expire)

    def get_media_with_metadata(self, media_id: str, title_id: str) -> dict[str, Any]:
        """
        Get media with metadata from redis

        Args:
            media_id: a unique identifier for the media
            title_id: a unique identifier for the title

        Returns:
            dict: a dictionary containing the media metadata (title_id, media_type, media_data)
        """
        metadata: dict = self.redis_client.hgetall(f'media:{media_id}:{title_id}')

        result = {
            "chat": metadata.get("title_id"),
            "media_type": metadata.get("media_type"),
            "file_bytes": metadata.get("media_data")
        }

        return result

    def close(self):
        self.redis_client.close()