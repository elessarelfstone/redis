import sys
import redis


key = sys.argv[1]
limit = int(sys.argv[2])

redis_client = redis.Redis()


for _ in range(limit):
    element = redis_client.lpop(key)
    if element is None:
        break
    sys.stdout.write(element.decode('utf-8') + '\n')
