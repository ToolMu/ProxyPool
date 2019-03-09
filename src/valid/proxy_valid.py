import requests

from src.utils.constant import VALID_URL, REQUESTS_TIMEOUT


class ProxyValid:
    @staticmethod
    def valid_proxy(proxy, channel):
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
                return True, proxy, channel
        except Exception as e:
            return False, e, None

        return False, "No Way", None
