import redis


class RedisConnection:
    def __init__(self, **kwargs):
        self.connection = redis.Redis(host=kwargs['HOST'], port=kwargs['PORT'], db=kwargs['db'])

    def get_all_keys(self):
        keys = self.connection.keys('*')
        for i in range(len(keys)):
            keys[i] = keys[i].decode('utf-8')
        return keys

    def set(self, key, value):
        if key in self.get_all_keys():
            return 'EXISTS'

        self.connection.set(key, value)
        return 'SUCCESSFUL'

    def get_by_key(self, key):
        if key not in self.get_all_keys():
            return 'NOT EXISTS'

        return self.connection.get(key).decode('utf-8')

