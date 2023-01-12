import time
from typing import Tuple


class Caching:

    def __init__(self, ttl, generator):
        self.ttl = ttl
        self.generator = generator
        self.cache = {}

    def store(self, key, value):
        self.cache[key] = (value, time.time()+self.ttl)

    def generate_value(self, key):

        def _create_params(key) -> Tuple:
            params = None
            if isinstance(key, str):
                params = (key,)
            elif isinstance(key, tuple):
                params = key
            else:
                params = (key,)
            return params

        params = _create_params(key)
        return self.generator(*params)

    def get(self, key):
        if key not in self.cache:
            value = self.generate_value(key)
            self.store(key, value)
            return value

        value, expires = self.cache[key]
        if time.time() > expires:
            value = self.generate_value(key)
            self.store(key, value)
            return value

        return value

    def update_value(self, key):
        params = (key,)
        value = self.generator(*params)
        self.cache[key] = (value, time.time() + self.ttl)

    def update_all_values(self):
        for key in self.cache:
            self.update_value(key)
