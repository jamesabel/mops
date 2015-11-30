
import collections
import pprint
import redis


class DB:
    def __init__(self, endpoint, password, verbose):
        self.endpoint = endpoint
        self.password = password
        self.port = 11920
        self.verbose = verbose
        if self.verbose:
            print('endpoint : %s' % endpoint)
            print('password : %s' % password)
        one_month = 30 * 24 * 60 * 60
        self.expire_time = one_month

    def set(self, computer_name, metrics):
        """
        set the metrics for one computer
        """
        r = redis.StrictRedis(self.endpoint, password=self.password, port=self.port)
        for k in metrics:
            full_key = 'computer:' + computer_name + ':' + k
            value = metrics[k]
            if self.verbose:
                print('set : %s=%s (ex=%i)' % (full_key, value, self.expire_time))
            r.set(full_key, value, ex=self.expire_time)

    def get(self):
        """
        get all the metrics for all the computers in the database
        """
        r = redis.StrictRedis(self.endpoint, password=self.password, port=self.port)
        d = collections.defaultdict(dict)
        for key in r.keys():
            computer_name, sub_key = self._disect_key(key.decode("utf-8"))
            if computer_name and sub_key:
                d[computer_name][sub_key] = r.get(key).decode("utf-8")
        if self.verbose:
            print('DB:get():')
            pprint.pprint(d)
        return d

    def dump(self):
        print('==== START DUMP ====')
        r = redis.StrictRedis(self.endpoint, password=self.password, port=self.port)
        for key in r.keys():
            val = r.get(key)
            print(key, val)
        print('==== END DUMP ====')

    def _disect_key(self, full_key):
        """
        convert the redis key to a computer name and the sub key
        e.g. 'computer:nuchsw1:disk:C:total' into 'nuchsw1' and 'disk:C:total'
        """
        computer_name = None
        sub_key = None
        k = full_key.split(":")
        if k[0] == 'computer':
            computer_name = k[1]
            sub_key = ':'.join(k[2:])
        return computer_name, sub_key