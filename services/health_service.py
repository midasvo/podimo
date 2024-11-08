import json
import time
from datetime import datetime
from typing import List
import httpx
from models.health_check import FeedHealthCheck

class HealthService:
    def __init__(self):
        with open('config/feeds.json') as f:
            self.config = json.load(f)
    
    async def check_feed_health(self, feed: dict) -> FeedHealthCheck:
        health_check = FeedHealthCheck(feed["id"], feed["name"])
        health_check.last_check = datetime.now()
        
        try:
            start_time = time.time()
            async with httpx.AsyncClient() as client:
                response = await client.get(feed["url"])
                end_time = time.time()
                
                health_check.response_time_ms = (end_time - start_time) * 1000
                health_check.is_healthy = response.status_code == 200
                
                if health_check.is_healthy:
                    health_check.last_success = datetime.now()
                else:
                    health_check.error_message = f"HTTP {response.status_code}"
                    
        except Exception as e:
            health_check.is_healthy = False
            health_check.error_message = str(e)
            
        return health_check
    
    async def check_all_feeds(self) -> List[FeedHealthCheck]:
        results = []
        for feed in self.config["feeds"]:
            result = await self.check_feed_health(feed)
            results.append(result)
        return results