import time
import pickle
from typing import Tuple, Dict
import logging


class Caching:

    def __init__(self, ttl: int, generator, cache_filename: str = None):
        self.ttl = ttl
        self.generator = generator
        self.cache = {}
        self.cache_filename = cache_filename
        self.load_from_file()

    def store(self, key, value):
        self.cache[key] = (value, time.time()+self.ttl)
        self.save_to_file()

    def save_to_file(self) -> None:
        if isinstance(self.cache_filename, str):
            try:
                with open(self.cache_filename, "wb") as cachefile:
                    pickle.dump(self.cache, cachefile)
                    logging.info('Cache is saved!')
            except pickle.PicklingError:
                logging.warning('There was an error saving cache! (%s)', self.cache_filename)
            except OSError:
                logging.warning('An error occured while writing the cache file: %s', self.cache_filename)

    def load_from_file(self) -> None:
        if isinstance(self.cache_filename, str):
            try:
                with open(self.cache_filename, "rb") as cachefile:
                    self.cache = pickle.load(cachefile)
                    logging.info('Cache loaded')
            except FileNotFoundError:
                logging.warning('Cache not loaded! File not found: %s', str(self.cache_filename))
            except pickle.UnpicklingError:
                logging.warning('Cache not loaded! There was an error during the loading process! (%s)', self.cache_filename)

    def flush(self):
        self.cache = {}
        self.save_to_file()

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

    def get_cache(self) -> Dict:
        return self.cache

    def update_value(self, key):
        params = (key,)
        value = self.generator(*params)
        self.store(key, value)
        #self.cache[key] = (value, time.time() + self.ttl)

    def update_all_values(self):
        for key in self.cache:
            self.update_value(key)
