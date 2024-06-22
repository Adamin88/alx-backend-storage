#!/usr/bin/env python3
"""
Caching request module
"""
import redis
import requests
from functools import wraps
from typing import Callable

# Initialize Redis client globally
client = redis.Redis()

def track_get_page(fn: Callable) -> Callable:
    """Decorator to cache the response and track the number of times the URL is accessed."""
    @wraps(fn)
    def wrapper(url: str) -> str:
        """Wrapper function to check cache, track access count, and fetch URL content."""
        # Increment the access count for the URL
        client.incr(f'count:{url}')
        
        # Check if the URL's content is already cached
        cached_page = client.get(f'cache:{url}')
        if cached_page:
            return cached_page.decode('utf-8')
        
        # If not cached, fetch the content using the original function
        response = fn(url)
        
        # Cache the fetched content with an expiration time of 10 seconds
        client.setex(f'cache:{url}', 10, response)
        
        return response
    return wrapper

@track_get_page
def get_page(url: str) -> str:
    """Fetches the HTML content of a URL."""
    response = requests.get(url)
    return response.text

# Example usage
if __name__ == "__main__":
    test_url = "http://slowwly.robertomurray.co.uk"
    print(get_page(test_url))

