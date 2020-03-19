import json

from redis import Redis

import src.config as config


class RedisObject:
    _prefix = 'base_object'

    def __init__(self):
        self._conn = self._get_conn()
        self.idx = None

    def _get_public_attributes(self):
        return {k: v for k, v in vars(self) if k[0] != '_'}

    @classmethod
    def _get_conn(cls):
        return Redis(config.redis)

    def create(self):
        self.idx = self._conn.incr(f"{self._prefix}/sequence")
        self._conn.set(f"{self._prefix}/{self.idx}", json.dumps(self._get_public_attributes()))
        return self.idx

    @classmethod
    def read_one(cls, idx):
        return json.loads(cls._get_conn().get(f"{cls._prefix}/{idx}"))

    @classmethod
    def read_many(cls):
        conn = cls._get_conn()
        return [type(cls)(json.loads(o)) for o in conn.mget(conn.keys(f"{cls._prefix}/*"))]

    def update(self):
        self._conn.set(f"{self._prefix}/{self.idx}", json.dumps(self._get_public_attributes()))

    @classmethod
    def delete(cls, idx):
        cls._get_conn().delete(f"{cls._prefix}/{idx}")

