import requests
from requests import Timeout
from lxml import etree

from src.utils.constant import REQUESTS_TIMEOUT
from src.utils.singleton import SingletonMetaClass


class ProxyRequests:
    """
    请求代理方法集合
    # TODO 日志
    """
    __metaclass__ = SingletonMetaClass

    def __init__(self):
        self._headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) AppleWebKit/537.36 (KHTML, like Gecko)',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        }

    def _get(self, url):
        try:
            return requests.get(url, headers=self._headers, timeout=REQUESTS_TIMEOUT)
        except Timeout as e:
            return ''
        except Exception as e:
            return ''
    
    def processed_html_tree(self, url):
        response = self._get(url)        
        return etree.HTML(response.content) if response and response.status_code == 200 else None

    def processed_re_str(self, url):
        response = self._get(url)        
        return response.text if response and response.status_code == 200 else ''
    

if __name__ == "__main__":
    import random
    import re

    
    def proxy_jiangxianli():
        page = random.randint(1, 10)
        url = 'http://ip.jiangxianli.com/?page={}'.format(page)

        html_tree = ProxyRequests().processed_html_tree(url)

        if html_tree is None:
            return 0

        tr_list = html_tree.xpath("/html/body/div[1]/div/div[1]/div[2]/table/tbody/tr")
        if len(tr_list) == 0:
            return 0

        for tr in tr_list:
            yield tr.xpath("./td[2]/text()")[0] + ":" + tr.xpath("./td[3]/text()")[0]


    def proxy_ip3366():
        page = random.randint(1, 10)
        url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)

        re_str = ProxyRequests().processed_re_str(url)

        proxies = re.findall(
            r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', 
            re_str
        )

        for proxy in proxies:
            yield ":".join(proxy)

    print(list(proxy_jiangxianli()))
    print(list(proxy_ip3366()))