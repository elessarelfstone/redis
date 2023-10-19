import sys

import redis


def make_dict_from_arr(arr, ):
    keys = arr[::2]
    values = arr[1::2]
    return dict(zip(keys, values))


args = sys.argv[1:]
client = redis.Redis()
ns_key = args.pop(0)

ns = client.incrby(ns_key)

# kvs = make_dict_from_arr(args)

for i, k in enumerate(args):
    client.set(f'{ns_key}-{ns}-{i}', k)


