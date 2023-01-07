import time


class Caching:

    def __init__(self, ttl, generator):
        self.ttl = ttl
        self.generator = generator
        self.cache = {}

    def get(self, key):
        if key in self.cache:
            value, expires = self.cache[key]
            if time.time() < expires:
                return value
        params = None
        if isinstance(key, str):
            params = (key,)
        elif isinstance(key, tuple):
            params = key
        else:
            params = (key,)
        value = self.generator(*params)
        self.cache[key] = (value, time.time() + self.ttl)
        return value
