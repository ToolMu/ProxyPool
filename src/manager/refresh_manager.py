import pymysql

from src.utils.singleton import SingletonMetaClass
from src.utils.constant import MYSQL_HOME, MYSQL_USER, MYSQL_PASSWD, MYSQL_PROXY_CHANNEL
from src.utils.constant import MAX_IP
from src.utils.constant import REFRESH_NUM

MAX_IP = 1


class RefreshManager(metaclass=SingletonMetaClass):

    def __init__(self):
        self._mysql_con = pymysql.connect(MYSQL_HOME, MYSQL_USER, MYSQL_PASSWD, MYSQL_PROXY_CHANNEL)

    def refresh(self):
        _mysql_cursor = self._mysql_con.cursor()

        _mysql_cursor.execute("SELECT count(*) FROM proxyip")
        if _mysql_cursor.fetchone()[0] < MAX_IP:
            return []

        select_sql = "SELECT ip_str, ip_channel FROM proxyip ORDER BY ip_in_time, ip_id LIMIT 0, {}".format(REFRESH_NUM)
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

        return refresh_ips, 'refresh_ip'


if __name__ == '__main__':
    from src.manager.raw_manager import ProductionManager

    refresh_data, refresh_channel = RefreshManager().refresh()
    ProductionManager().production(refresh_data, refresh_channel)
    print("OK!")
