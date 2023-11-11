import sys
import redis


def safe_increase(redis, key, increment):
    with redis.pipeline() as pipe:
        while True:
            try:
                pipe.watch(key)

                current_value = pipe.get(key)
                current_value = int(current_value) if current_value else 0
                new_value = current_value + increment

                pipe.multi()
                pipe.set(key, new_value)
                pipe.execute()

                return new_value
            except redis.WatchError:
                continue


key = sys.argv[1]
increment_value = int(sys.argv[2])

redis = redis.Redis()

new_value = safe_increase(redis, key, increment_value)
