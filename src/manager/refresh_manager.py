import pymysql

from src.utils.singleton import SingletonMetaClass
from src.utils.constant import MYSQL_HOME, MYSQL_USER, MYSQL_PASSWD, MYSQL_PROXY_CHANNEL
from src.utils.constant import REFRESH_NUM


class RefreshManager:
    __metaclass__ = SingletonMetaClass

    def __init__(self):
        self._mysql_con = pymysql.connect(MYSQL_HOME, MYSQL_USER, MYSQL_PASSWD, MYSQL_PROXY_CHANNEL)

    def refresh(self):
        _mysql_cursor = self._mysql_con.cursor()

        select_sql = "SELECT ip_str FROM proxyip ORDER BY ip_in_time, ip_id LIMIT 0, {}".format(REFRESH_NUM)
        _mysql_cursor.execute(select_sql)
        refresh_ips = []

        for item in _mysql_cursor.fetchall():
            delete_sql = "DELETE FROM proxyip WHERE ip_str='{}'".format(item[0])
            try:
                _mysql_cursor.execute(delete_sql)
                self._mysql_con.commit()
                refresh_ips.append(item[0])
            except Exception as e:
                self._mysql_con.rollback()

        for item in refresh_ips:
            yield item


if __name__ == '__main__':
    from src.manager.raw_manager import ProductionManager

    refresh_data = RefreshManager().refresh()
    ProductionManager().production(refresh_data)
    print("OK!")
