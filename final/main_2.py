import sys
import hashlib
import redis


def calculate_sha1_hash(filepath):
    sha1 = hashlib.sha1()
    try:
        with open(filepath, 'rb') as file:
            while True:
                data = file.read(8192)
                if not data:
                    break
                sha1.update(data)
        return sha1.hexdigest()
    except IOError:
        print(f"Ошибка при чтении файла: {filepath}")
        return None


def main(namespace):
    redis_client = redis.Redis()

    while True:
        file = redis_client.brpoplpush(f"{namespace}:job", f"{namespace}:job", 0)
        if file:
            file = file.decode('utf-8')
            sha1_hash = calculate_sha1_hash(file)
            if sha1_hash:
                redis_client.set(f"{namespace}:res:{file}", sha1_hash)
                redis_client.lpush(f"{namespace}:res", 'done')
                redis_client.lrem(f"{namespace}:job", 0, file)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    ns = sys.argv[1]
    main(ns)
