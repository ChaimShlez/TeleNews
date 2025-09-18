from typing import Any, Optional

import redis
from utils.logger.logger import Logger

logger = Logger.get_logger()


class RedisService:
    def __init__(self, host: str, port: int = 6379):
        """Initialize the Redis client"""
        try:
            self.redis_client = redis.Redis(host=host, port=port, decode_responses=False)
            # Test connection
            self.redis_client.ping()
            logger.info(f"Connected to Redis at {host}:{port}")
        except redis.ConnectionError as e:
            logger.error(f"Failed to connect to Redis: {e}")
            raise

    def save_media_with_metadata(
            self,
            media_id: str,
            title_id: str,
            media_type: str,
            media_data: bytes,
            expire: int = 86400
    ) -> bool:
        """
        Save media with metadata in Redis with expiration time

        Args:
            media_id: a unique identifier for the media
            title_id: a unique identifier for the title
            media_type: the type of the media
            media_data: the media data in bytes
            expire: the expire time in seconds
        """
        try:
            hash_name = f'media:{media_id}:{title_id}'

            # Save all data at once using pipeline
            pipe = self.redis_client.pipeline()
            pipe.hset(hash_name, mapping={
                "title_id": title_id,
                "media_type": media_type,
                "media_data": media_data
            })
            pipe.expire(hash_name, expire)
            pipe.execute()

            logger.info(f"Saved to Redis: {media_id}, {title_id}")
            return True

        except Exception as e:
            logger.error(f"Error saving to Redis: {e}")
            return False

    def get_media_with_metadata(self, media_id: str, title_id: str) -> Optional[dict[str, Any]]:
        """
        Retrieve media with metadata from Redis

        Args:
            media_id: the media identifier
            title_id: the title identifier

        Returns:
            Dictionary with the data or None if not found
        """
        try:
            hash_name = f'media:{media_id}:{title_id}'

            # Check if key exists
            if not self.redis_client.exists(hash_name):
                logger.warning(f"Key does not exist: {hash_name}")
                return None

            metadata: dict = self.redis_client.hgetall(hash_name)

            if not metadata:
                logger.warning(f"No data found for: {media_id}, {title_id}")
                return None

            logger.info(f"Retrieved from Redis: {media_id}, {title_id}")

            # Convert bytes to string (except for media_data)
            result = {
                "title_id": metadata.get(b"title_id").decode('utf-8') if metadata.get(b"title_id") else None,
                "media_type": metadata.get(b"media_type").decode('utf-8') if metadata.get(b"media_type") else None,
                "media_data": metadata.get(b"media_data")  # bytes remain as bytes
            }

            return result

        except Exception as e:
            logger.error(f"Error retrieving from Redis: {e}")
            return None

    def delete_media(self, media_id: str, title_id: str) -> bool:
        """Delete media from Redis"""
        try:
            hash_name = f'media:{media_id}:{title_id}'
            result = self.redis_client.delete(hash_name)
            logger.info(f"Deleted from Redis: {media_id}, {title_id}")
            return bool(result)
        except Exception as e:
            logger.error(f"Error deleting from Redis: {e}")
            return False

    def check_media_exists(self, media_id: str, title_id: str) -> bool:
        """Check if media exists in Redis"""
        try:
            hash_name = f'media:{media_id}:{title_id}'
            return self.redis_client.exists(hash_name) > 0
        except Exception as e:
            logger.error(f"Error checking existence: {e}")
            return False

    def get_ttl(self, media_id: str, title_id: str) -> int:
        """Get remaining time to live for the key"""
        try:
            hash_name = f'media:{media_id}:{title_id}'
            return self.redis_client.ttl(hash_name)
        except Exception as e:
            logger.error(f"Error getting TTL: {e}")
            return -2

    def close(self):
        """Close the Redis connection"""
        try:
            self.redis_client.close()
            logger.info("Redis connection closed")
        except Exception as e:
            logger.error(f"Error closing connection: {e}")