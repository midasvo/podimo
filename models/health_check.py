from datetime import datetime
from typing import Optional

class FeedHealthCheck:
    def __init__(self, feed_id: str, feed_name: str):
        self.feed_id = feed_id
        self.feed_name = feed_name
        self.last_check: Optional[datetime] = None
        self.last_success: Optional[datetime] = None
        self.response_time_ms: Optional[float] = None
        self.is_healthy: bool = False
        self.error_message: Optional[str] = None

    def to_dict(self):
        return {
            "feed_id": self.feed_id,
            "feed_name": self.feed_name,
            "last_check": self.last_check.isoformat() if self.last_check else None,
            "last_success": self.last_success.isoformat() if self.last_success else None,
            "response_time_ms": self.response_time_ms,
            "is_healthy": self.is_healthy,
            "error_message": self.error_message
        } 