#!/usr/bin/env python3
"""
Caching request module
"""
from flask import Flask, request
import redis


app = Flask(__name__)
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)

@app.route('/some_url')
def count_url_access():
    url = request.url

    # Check if the URL's count is already cached
    cache_key = f"count:{url}"
    count = redis_client.get(cache_key)

    if count is not None:
        # If count is cached, return it
        count = int(count)
    else:
        # If count is not cached, get it from the data store and cache it
        # Replace this with your own logic to get the count from the data store
        count = get_count_from_data_store(url)
        
        # Cache the count with an expiration time of 10 seconds
        redis_client.setex(cache_key, 10, count)

    # Increment the count and update the cache
    count += 1
    redis_client.setex(cache_key, 10, count)

     return f"This URL has been accessed {count} times."

 def get_count_from_data_store(url):
    # Replace this function with your own logic to get the count from the data store
    # For example, you might query a database or fetch the count from another source
    # For this example, let's assume we're just returning 0.
    return 0

if __name__ == '__main__':
    app.run()
