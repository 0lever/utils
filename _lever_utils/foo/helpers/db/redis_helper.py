# -*- coding: utf-8 -*-
from functools import wraps
import hashlib
import logging
import json
import redis


class MyRedis(object):
    def __init__(self, host, port, password,db=0):
        self.pool = redis.ConnectionPool(host=host, password=password, port=port, db=db)
        self.rs = redis.Redis(connection_pool=self.pool, db=db)

    def get_redis(self):
        return self.rs


def redising(time=0, redis_key_prefix="_lever_utils", db=None):
    '''
    redis 装饰器
    :param time: 保留时常
    # time==0,则不走缓存;
    # time>0,则走缓存,缓存时间为time;
    # time==-1,则走缓存，缓存时间为永久.
    # time==-2,则每次现查，并永久缓存覆盖现有缓存
    :param redis_key: redis key
    :return:
    '''
    def func_wrapper(func):
        @wraps(func)
        def return_wrapper(*args, **kwargs):
            if time == 0 or db is None:
                return func(*args, **kwargs), None
            func_info_str = "model[%s]\t func[%s]\t file[%s][%s]\t args[%s]\t kwargs[%s]" % (func.__module__
                                                                                             , func.__name__
                                                                                             , func.func_code.co_filename
                                                                                             , func.func_code.co_firstlineno
                                                                                             , args
                                                                                             , kwargs)
            m2 = hashlib.md5()
            m2.update(func_info_str.encode('utf-8'))
            func_info_str_md5 = m2.hexdigest()
            func_info_str_md5_redis_key = redis_key_prefix+"-"+func_info_str_md5
            redis_store = db
            if time == -1 or time > 0:
                redis_result = redis_store.get(func_info_str_md5_redis_key)
                if redis_result is None:
                    func_result = func(*args, **kwargs)
                    redis_store.set(func_info_str_md5_redis_key, json.dumps(func_result), time if time > 0 else None)
                else:
                    logging.info("to-redis:key[%s]" % func_info_str_md5_redis_key)
                    func_result = json.loads(redis_result)
            else:
                func_result = func(*args, **kwargs)
                redis_store.set(func_info_str_md5_redis_key, json.dumps(func_result))
            return func_result, func_info_str_md5_redis_key
        return return_wrapper
    return func_wrapper