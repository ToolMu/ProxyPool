import time
import pickle
from random import sample, seed
from collections import Generator

import redis

from src.utils.singleton import SingletonMetaClass
from src.get.raw_proxy_get import RawProxyGetter
from src.utils.log_handler import Logger
from src.utils.constant import REDIS_HOST, REDIS_PRODUCTION_CHANNEL


class ProductionManager(metaclass=SingletonMetaClass):

    def __init__(self):
        self._connect_pool = redis.ConnectionPool(host=REDIS_HOST)

    def production(self, iterator, channel):
        if isinstance(iterator, Generator):
            iterator = list(iterator)

        redis_con = redis.Redis(connection_pool=self._connect_pool)
        log_handler = Logger("ProxyPool").get_log()

        for item in iterator:
            redis_con.lpush(REDIS_PRODUCTION_CHANNEL, pickle.dumps((item, channel)))

        log_handler.info("[ProductionManager] add to the mq: {}".format(iterator))


class GetterManager(metaclass=SingletonMetaClass):

    def __init__(self):
        self._channels = {
            "jiangxianli": RawProxyGetter.proxy_jiangxianli,
            "ip3366": RawProxyGetter.proxy_ip3366,
            "kuaidaili": RawProxyGetter.proxy_kuaidaili,
            "xicidaili": RawProxyGetter.proxy_xicidaili,
        }

    def random_proxy_get(self):
        log_handler = Logger("ProxyPool").get_log()
        seed(time.time())

        choose_channel = sample(self._channels.keys(), 1)[0]
        log_handler.info("[GetterManager] >> The channel is {}".format(choose_channel))

        return self._channels[choose_channel](), choose_channel

    def specially_proxy_get(self, channel):
        return self._channels[channel](), channel


if __name__ == '__main__':
    # print(list(GetterManager().random_proxy_get()))
    # time.sleep(3)
    # print(list(GetterManager().random_proxy_get()))
    # print(list(GetterManager().specially_proxy_get('kuaidaili')))
    # proxy_ips = GetterManager().specially_proxy_get('kuaidaili')
    proxy_ips, proxy_channel = GetterManager().random_proxy_get()
    ProductionManager().production(proxy_ips, proxy_channel)
    print("OK!")
