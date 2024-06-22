import requests
import redis
from functools import wraps
import time

# Initialize Redis client
r = redis.Redis()

def cache_with_count(expiration=10):
    """Decorator to cache the page content and count URL accesses."""
    def decorator(func):
        @wraps(func)
        def wrapper(url, *args, **kwargs):
            count_key = f"count:{url}"
            cache_key = f"cache:{url}"

            # Increment the access count
            r.incr(count_key)

            # Check if the result is already cached
            cached_result = r.get(cache_key)
            if cached_result:
                return cached_result.decode('utf-8')

            # Call the actual function and get the result
            result = func(url, *args, **kwargs)

            # Cache the result with an expiration time
            r.setex(cache_key, expiration, result)
            
            return result
        return wrapper
    return decorator

@cache_with_count(expiration=10)
def get_page(url: str) -> str:
    """Fetches the HTML content of a URL."""
    response = requests.get(url)
    return response.text

# Example usage
if __name__ == "__main__":
    test_url = "http://slowwly.robertomurray.co.uk"
    print(get_page(test_url))
    time.sleep(5)  # Wait for 5 seconds
    print(get_page(test_url))
    time.sleep(11)  # Wait for another 11 seconds (total 16 seconds from start)
    print(get_page(test_url))

