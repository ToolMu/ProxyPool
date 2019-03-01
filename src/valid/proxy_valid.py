import requests
import pymysql

from src.utils.constant import VALID_URL, REQUESTS_TIMEOUT


class ProxyValid:
    @staticmethod
    def valid_proxy(proxy):
        """
        检验代理是否可用
        """
        if isinstance(proxy, bytes):
            proxy = proxy.decode('utf8')

        proxies = {
            "http": "http://{proxy}".format(proxy=proxy)
        }

        try:
            response = requests.get(VALID_URL, proxies=proxies, timeout=REQUESTS_TIMEOUT, verify=False)
            if response.status_code == 200 and response.json().get("origin"):
                return True, proxy
        except Exception as e:
            pass

        return False, None


if __name__ == '__main__':
    http_proxy = "212.83.145.167:54321"
    print(ProxyValid.valid_proxy(http_proxy))
