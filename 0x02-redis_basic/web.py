#!/usr/bin/env python3
"""
Web module for fetching and caching web pages.
"""
import requests
import redis
import time
from functools import wraps

# Connect to Redis
r = redis.Redis(host='localhost', port=6379, db=0)

def cache_page(func):
    """
    Decorator to cache the result of get_page.
    """
    @wraps(func)
    def wrapper(url):
        cache_key = f"page:{url}"
        count_key = f"count:{url}"
        
        # Check if the cached page exists
        cached_page = r.get(cache_key)
        if cached_page:
            # Increment the access count
            r.incr(count_key)
            return cached_page.decode('utf-8')  # Decode bytes to string
        
        # If not cached, call the original function
        page_content = func(url)
        
        # Cache the result with an expiration time of 10 seconds
        r.setex(cache_key, 10, page_content)
        # Increment the access count
        r.incr(count_key)
        return page_content

    return wrapper

@cache_page
def get_page(url: str) -> str:
    """
    Fetch the HTML content of a URL.
    """
    response = requests.get(url)
    return response.text

if __name__ == "__main__":
    # Example usage
    url = "http://slowwly.robertomurray.co.uk/delay/10000/url/http://www.google.com"
    print(get_page(url))
