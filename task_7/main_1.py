import os
import sys
import redis


base_path = sys.argv[1]
redis = redis.Redis()
pipeline = redis.pipeline()

for key in redis.scan_iter(f"data:{base_path}/*"):
    pipeline.delete(key)
pipeline.delete(f"data:{base_path}")
pipeline.execute()


def is_readable_file(filepath):
    return os.path.isfile(filepath) and os.access(filepath, os.R_OK)


def save_file_content_to_redis(pipeline, root, file):
    full_path = os.path.join(root, file)
    key = f"data:{full_path}"

    with open(full_path, 'rb') as file:
        content = file.read()
    pipeline.set(key, content)


for root, dirs, files in os.walk(base_path):
    for file in files:
        full_path = os.path.join(root, file)
        if is_readable_file(full_path):
            save_file_content_to_redis(pipeline, root, file)

pipeline.execute()
