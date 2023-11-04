import os

import sys
from collections import deque

import redis

SIZE = 100
FILE_PATH = sys.argv[1]


def tail_c(filename, n, block_size=1024):

    buffer = deque(maxlen=2)

    with open(filename, 'rb') as f:

        # storage for last n bytes
        last_n_bytes = deque(maxlen=n)

        while True:
            block = f.read(block_size)

            if not block:
                break

            buffer.append(block)

    return b"".join(buffer)[-n:]


client = redis.Redis()
key = os.path.basename(FILE_PATH)
tail = client.get(key)

if not tail:
    tail = tail_c(FILE_PATH, SIZE, 2048 * 2048)
    client.set(key, tail)

sys.stdout.buffer.write(tail)
