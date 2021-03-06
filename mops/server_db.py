
import redis
import json
import os
import time

import mops.util
import mops.logger


def dict_to_kv(input_dict, _out=None, _base_string=None):
    """
    convert a hierarchical dict of dicts to a dict of key/value pairs for redis
    :param input_dict: input dict
    :param _out: output list of strings (used during recursion)
    :param _base_string: base of current string (used for recursion)
    :return: a dict of key-value strings
    """
    if _out is None:
        _out = {}
    for elem in input_dict:
        assert(":" not in elem)
        val = input_dict[elem]
        if type(val) is dict:
            if _base_string:
                dict_to_kv(val, _out, _base_string + ':' + elem)
            else:
                dict_to_kv(val, _out, elem)
        else:
            if _base_string:
                _out[_base_string + ':' + elem] = str(val)
            else:
                _out[elem] = str(val)
    return _out


def kv_to_dict(input_kv):
    """
    convert a dict with colon delimited key value pairs to a hierarchical dict
    :param input_kv: key/value pairs delimited with a colon
    :return: hierarchical dict
    """

    od = {}
    for k in input_kv:
        v = input_kv[k]
        o = od
        while ":" in k:
            l, r = k.split(':', 1)
            if l not in o:
                o[l] = {}
            o = o[l]
            k = r
        o[k] = v
    return od


class ServerDB:
    """
    communicate with the database
    """
    def __init__(self, endpoint, password):
        self.endpoint = endpoint
        self.password = password
        self.port = 11920

        mops.logger.log.debug('endpoint : %s' % endpoint)
        one_day = 24 * 60 * 60
        one_month = one_day * 30
        self.expire_time = one_month

    def set(self, metrics):
        """
        set the metrics for one or more computers
        :param metrics: hierarchical dict of metrics
        """
        mops.logger.log.debug('DB set')
        r = redis.StrictRedis(self.endpoint, password=self.password, port=self.port)
        kv_metrics = dict_to_kv(metrics)
        for k in kv_metrics:
            mops.logger.log.debug('db:set:%s:%s (ex=%i)' % (k, kv_metrics[k], self.expire_time))
            try:
                r.set(k, kv_metrics[k], ex=self.expire_time)
            except redis.exceptions.ConnectionError as e:
                mops.logger.log.warn(str(e))
                break

    def get(self):
        """
        get all the metrics for all the computers in the database in the form of a hierarchical dict
        """
        r = redis.StrictRedis(self.endpoint, password=self.password, port=self.port)
        kv = {}
        try:
            keys = [k for k in r.scan_iter('*')]
        except redis.exceptions.ConnectionError as e:
            mops.logger.log.warn(str(e))
            keys = []
        if len(keys) > 0:
            for key in keys:
                k = key.decode("utf-8")
                v = r.get(key).decode("utf-8")
                mops.logger.log.debug("db:get:%s:%s" % (k,v))
                kv[k] = v
            kv['timestamp'] = time.time()
            with open(mops.util.get_cache_file_path(), 'w') as f:
                json.dump(kv, f, indent=2)
        elif os.path.exists(mops.util.get_cache_file_path()):
            with open(mops.util.get_cache_file_path()) as f:
                mops.logger.log.warn('could not access redis, getting values from cache file (%s)' % mops.util.get_cache_file_path())
                kv = json.load(f)
        return kv_to_dict(kv)


