import time
from random import sample, seed

import redis

from src.utils.singleton import SingletonMetaClass
from src.get.raw_proxy_get import RawProxyGetter

from src.utils.constant import REDIS_HOST, REDIS_PRODUCTION_CHANNEL


class ProductionManager:
    __metaclass__ = SingletonMetaClass

    def __init__(self):
        self._connect_pool = redis.ConnectionPool(host=REDIS_HOST)

    def production(self, iterator):
        redis_con = redis.Redis(connection_pool=self._connect_pool)
        for item in iterator:
            redis_con.lpush(REDIS_PRODUCTION_CHANNEL, item)


class GetterManager:
    __metaclass__ = SingletonMetaClass

    def __init__(self):
        self._channels = {
            "jiangxianli": RawProxyGetter.proxy_jiangxianli,
            "ip3366": RawProxyGetter.proxy_ip3366,
            "kuaidaili": RawProxyGetter.proxy_kuaidaili,
            "xicidaili": RawProxyGetter.proxy_xicidaili,
        }

    def random_proxy_get(self):
        seed(time.time())
        choose_channel = sample(self._channels.keys(), 1)[0]
        return self._channels[choose_channel]()

    def specially_proxy_get(self, channel):
        return self._channels[channel]()


if __name__ == '__main__':
    # print(list(GetterManager().random_proxy_get()))
    # time.sleep(3)
    # print(list(GetterManager().random_proxy_get()))
    # print(list(GetterManager().specially_proxy_get('kuaidaili')))
    # proxy_ips = GetterManager().specially_proxy_get('kuaidaili')
    proxy_ips = GetterManager().random_proxy_get()
    ProductionManager().production(proxy_ips)
    print("OK!")
