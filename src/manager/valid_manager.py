import time

import redis
import pymysql

from src.utils.thread_pool import ThreadPool
from src.valid.proxy_valid import ProxyValid
from src.utils.constant import THREADNUM, REDIS_HOST, REDIS_PRODUCTION_CHANNEL
from src.utils.constant import MYSQL_HOME, MYSQL_USER, MYSQL_PASSWD, MYSQL_PROXY_CHANNEL


class ValidManager:
    def __init__(self):
        self._connect_pool = redis.ConnectionPool(host=REDIS_HOST)
        self._mysql_con = pymysql.connect(MYSQL_HOME, MYSQL_USER, MYSQL_PASSWD, MYSQL_PROXY_CHANNEL)

        self._valid_pool = ThreadPool(THREADNUM)

    def consumption(self):
        while True:
            rcon = redis.Redis(connection_pool=self._connect_pool)
            proxy_task = rcon.blpop(REDIS_PRODUCTION_CHANNEL, 0)[1]
            self._valid_pool.add(ProxyValid.valid_proxy, (proxy_task,), self._save)

    def _save(self, status):
        if status is not None and isinstance(status, tuple) and status[0]:
            insert_sql = "INSERT INTO {base_name}.proxyip (ip_str, ip_in_time) VALUES ('{ip_info}', '{new_time}')".format(
                base_name=MYSQL_PROXY_CHANNEL, ip_info=status[1], new_time=str(time.time())
            )
            _mysql_cursor = self._mysql_con.cursor()
            try:
                _mysql_cursor.execute(insert_sql)
                self._mysql_con.commit()
            except Exception as e:
                self._mysql_con.rollback()


if __name__ == '__main__':
    ValidManager().consumption()
