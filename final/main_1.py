import sys
import redis


def main(namespace, files):

    redis_client = redis.Redis()

    for file in files:
        redis_client.lpush(f"{namespace}:job", file)

    while files:

        keys = [f"{namespace}:res:{file}" for file in files]
        results = redis_client.mget(keys)

        if not any(results):

            result = redis_client.blpop(f"{namespace}:res", 3)
            if result:
                key, value = result
                file = key.decode('utf-8').split(':')[-1]
                print(f"{file} {value.decode('utf-8')}")
                files.remove(file)
        else:

            for file, res in zip(files, results):
                if res is not None:
                    print(f"{file} {res.decode('utf-8')}")
                    files.remove(file)


if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)

    ns = sys.argv[1]
    file_paths = sys.argv[2:]
    main(ns, file_paths)