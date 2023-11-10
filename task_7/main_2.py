import redis


redis = redis.Redis()
keys = redis.keys('data:*')

for key in keys:
    size = redis.strlen(key)
    filename = key.decode('utf-8')[5:]
    print(f"{size} {filename}")
