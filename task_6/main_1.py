import sys
import redis


redis = redis.Redis()


key = sys.argv[1]

for line in sys.stdin:

    line = line.rstrip('\n')
    redis.rpush(key, line)
    redis.ltrim(key, -20, -1)
