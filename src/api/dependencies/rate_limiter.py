from fastapi import HTTPException, Request
from src.services.redis_client import redis_client
from typing import Callable

class RateLimiter:
    def __init__(self, times: int, seconds: int):
        """
        Initialize the RateLimiter.

        Args:
            times (int): Number of allowed requests.
            seconds (int): Time window in seconds.
        """
        self.times = times
        self.seconds = seconds

    async def __call__(self, request: Request):
        """
        Call method to enforce rate limiting.

        Args:
            request (Request): The incoming request.

        Raises:
            HTTPException: If the rate limit is exceeded.
        """
        client_ip = request.client.host
        key = f"rate_limit:{client_ip}"
        
        current = redis_client.get(key)
        
        if current is None:
            redis_client.set(key, 1, ex=self.seconds)
        elif int(current) >= self.times:
            raise HTTPException(
                status_code=429, 
                detail="Rate limit exceeded. Please try again later."
            )
        else:
            redis_client.incr(key)
        
        return True

def rate_limit(times: int = 10, seconds: int = 60) -> Callable:
    """
    Factory function to create a RateLimiter instance.

    Args:
        times (int, optional): Number of allowed requests. Defaults to 10.
        seconds (int, optional): Time window in seconds. Defaults to 60.

    Returns:
        Callable: A RateLimiter instance.
    """
    return RateLimiter(times, seconds)
