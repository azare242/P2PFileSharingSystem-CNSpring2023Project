import redis


class RedisConnection:
    def __init__(self, **kwargs):
        self.pool = redis.ConnectionPool(host=kwargs['HOST'], port=kwargs['PORT'], db=kwargs['db'])

    def get_all_keys(self):
        connection = redis.Redis(connection_pool=self.pool)
        keys = connection.keys('*')
        for i in range(len(keys)):
            keys[i] = keys[i].decode('utf-8')
        return keys

    def set(self, key, value):

        connection = redis.Redis(connection_pool=self.pool)
        connection.set(key, value)
        return 'SUCCESSFUL'

    def get_by_key(self, key):
        if key not in self.get_all_keys():
            return 'NOT EXISTS'

        connection = redis.Redis(connection_pool=self.pool)
        return connection.get(key).decode('utf-8')
