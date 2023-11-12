import sys
import redis


def valid_pattern(s):
    return s[7] >= '3' and all(s[i] == '0' for i in [1, 3, 5, 9])


name = sys.argv[1]

redis_client = redis.Redis()
pubsub = redis_client.pubsub()

pattern = f"{name}:*"
pubsub.psubscribe(pattern)

for message in pubsub.listen():
    if message['type'] == 'pmessage':
        channel = message['channel'].decode('utf-8')
        _, formatted_number = channel.split(':')

        if valid_pattern(formatted_number):
            print(message['data'].decode('utf-8'))
            break

pubsub.close()
