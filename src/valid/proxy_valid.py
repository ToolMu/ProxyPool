import requests

from src.utils.constant import VALID_URL, REQUESTS_TIMEOUT

class ProxyValid:
    @staticmethod
    def valid_proxy(proxy, logger):
        """
        检验代理是否可用
        """
        if isinstance(proxy, bytes):
            proxy = proxy.decode('utf8')

        proxies = {
            "http": "http://{proxy}".format(proxy=proxy)
        }
        header = {
            "Connection": "close"
        }

        try:
            response = requests.get(VALID_URL, headers=header, proxies=proxies, timeout=REQUESTS_TIMEOUT, verify=False)
            if response.status_code == 200 and response.json().get("origin"):
                return True, proxy
        except Exception as e:
            return False, e

        return False, "No why"


if __name__ == '__main__':
    http_proxy = "212.83.145.167:54321"
    print(ProxyValid.valid_proxy(http_proxy))
