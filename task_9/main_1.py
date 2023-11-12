import sys
import redis
import random
from collections import Counter


def format_number(n):
    counter = Counter(str(n))
    return ''.join(str(counter.get(str(digit), 0)) for digit in range(10))


channel_name = sys.argv[1]

redis = redis.Redis()

while True:
    n = random.randint(0, 999999999)
    formatted_number = format_number(n)
    channel = f"{channel_name}:{formatted_number}"
    redis.publish(channel, n)
