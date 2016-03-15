import redis
from redis.sentinel import Sentinel
from redis.client import StrictPipeline
import redis.client


class RedisHelper(object):
    def __init__(self, host: str, port: int, is_sentinel=False, sentinel_service=None):
        self.host = host
        self.port = port
        self.is_sentinel = is_sentinel
        self.sentinel_service = sentinel_service

    def get_connection(self, is_read_only=False) -> redis.StrictRedis:
        """
        Gets a StrictRedis connection for normal redis or for redis sentinel based upon redis mode in configuration.

        :type is_read_only: bool
        :param is_read_only: In case of redis sentinel, it returns connection to slave

        :return: Returns a StrictRedis connection
        """
        if self.is_sentinel:
            sentinel = Sentinel([(self.host, self.port)])
            if is_read_only:
                connection = sentinel.slave_for(self.sentinel_service, decode_responses=True)
            else:
                connection = sentinel.master_for(self.sentinel_service, decode_responses=True)
        else:
            connection = redis.StrictRedis(host=self.host, port=self.port, decode_responses=True)
        return connection

    def get_atomic_connection(self) -> StrictPipeline:
        """
        Gets a StrictPipeline for normal redis or for redis sentinel based upon redis mode in configuration

        :return: Returns a StrictPipeline object
        """
        if self.is_sentinel:
            sentinel = Sentinel([(self.host, self.port)])
            pipeline = sentinel.master_for(self.sentinel_service, decode_responses=True).pipeline(True)
        else:
            pipeline = redis.StrictRedis(host=self.host, port=self.port, decode_responses=True).pipeline(True)
        return pipeline
