import base64
import sys
from collections import deque

import redis

KEY = 'tail100'
SIZE = 100



def tail(n):

    def bytes_from_file(fpath, chunksize=8192):
        with open(fpath, "rb") as f:
            while True:
                chunk = f.read(chunksize)
                if chunk:
                    yield chunk
                else:
                    break

    f_path = sys.argv[1]
    client = redis.Redis()

    t = client.get(KEY)
    r = b''
    if not t:
        d = deque(maxlen=2)
        for ch in bytes_from_file(f_path):
            d.append(ch)

        buff = d[0] + d[1]
        buff = buff[-100:]
        buff = base64.b64encode(buff)
        client.set(KEY, buff)
        r = buff
    else:
        r = t

    return r


print(base64.b64decode(tail(SIZE)).decode('utf-8'), file=sys.stdout)
