import os

import sys
from collections import deque

import redis

SIZE = 100
FILE_PATH = sys.argv[1]


def tail_c(filename, n, block_size=1024):

    with open(filename, 'rb') as f:

        # storage for last n bytes
        last_n_bytes = deque(maxlen=n)

        while True:
            block = f.read(block_size)
            if not block:
                break
            for byte in block:
                last_n_bytes.append(byte)

    return bytes(last_n_bytes)


client = redis.Redis()
key = os.path.basename(FILE_PATH)
tail = client.get(key)

if not tail:
    tail = tail_c(FILE_PATH, SIZE, 1024 * 1024)
    client.set(key, tail)

sys.stdout.buffer.write(tail)
