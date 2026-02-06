import redis
import json
from typing import Optional, Any
from app.config import get_settings

settings = get_settings()


class CacheService:
    def __init__(self):
        try:
            self.redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)
            # Test connection
            self.redis_client.ping()
            self.enabled = True
        except Exception as e:
            print(f"Redis connection failed: {e}. Running without cache.")
            self.redis_client = None
            self.enabled = False

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        if not self.enabled:
            return None

        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Cache get error: {e}")
            return None

    def set(self, key: str, value: Any, ttl: int = 86400) -> bool:
        """
        Set value in cache with TTL (default 24 hours)
        ttl in seconds
        """
        if not self.enabled:
            return False

        try:
            serialized = json.dumps(value, default=str)
            self.redis_client.setex(key, ttl, serialized)
            return True
        except Exception as e:
            print(f"Cache set error: {e}")
            return False

    def delete(self, key: str) -> bool:
        """Delete key from cache"""
        if not self.enabled:
            return False

        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            print(f"Cache delete error: {e}")
            return False

    def get_stock_analysis(self, symbol: str) -> Optional[dict]:
        """Get cached stock analysis"""
        return self.get(f"stock_analysis:{symbol}")

    def set_stock_analysis(self, symbol: str, data: dict) -> bool:
        """Cache stock analysis for 24 hours"""
        return self.set(f"stock_analysis:{symbol}", data, ttl=86400)


# Global cache instance
cache_service = CacheService()
