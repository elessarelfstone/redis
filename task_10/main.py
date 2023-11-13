import sys
import redis

count = int(sys.argv[1])
keys = sys.argv[2:]


redis = redis.Redis()

try:
    for _ in range(count):

        item = redis.blpop(keys, timeout=5)
        if item is None:
            print("Timeout reached. Exiting.")
            sys.exit(1)
        key, value = item
        print(f"{key.decode('utf-8')} {value.decode('utf-8')}")
except Exception as e:
    print(f"An error occurred: {e}")
    sys.exit(1)
