import re
import random

from src.utils.base_requests import ProxyRequests


class RawProxyGetter:
    
    @staticmethod
    def proxy_jiangxianli():
        """
        http://ip.jiangxianli.com/
        """
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

    @staticmethod
    def proxy_ip3366():
        """
        http://www.ip3366.net/free/
        """
        page = random.randint(1, 10)
        url = 'http://www.ip3366.net/free/?stype=1&page={}'.format(page)

        re_str = ProxyRequests().processed_re_str(url)

        proxies = re.findall(
            r'<td>(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})</td>[\s\S]*?<td>(\d+)</td>', 
            re_str
        )

        for proxy in proxies:
            yield ":".join(proxy)

    @staticmethod
    def proxy_kuaidaili():
        """
        https://www.kuaidaili.com/free/inha/1/
        """
        page = random.randint(1, 10)
        url = 'https://www.kuaidaili.com/free/inha/{}/'.format(page)

        html_tree = ProxyRequests().processed_html_tree(url)
        if html_tree is None:
            return 0

        proxy_list = html_tree.xpath('.//table//tr')
        for tr in proxy_list[1:]:
            yield ':'.join(tr.xpath('./td/text()')[0:2])

    @staticmethod
    def proxy_xicidaili():
        """
        http://www.xicidaili.com
        """
        page = random.randint(1, 10)
        url = 'http://www.xicidaili.com/nn/{}'.format(page)

        html_tree = ProxyRequests().processed_html_tree(url)
        if html_tree is None:
            return 0

        proxy_list = html_tree.xpath('.//table[@id="ip_list"]//tr[position()>1]')
        for proxy in proxy_list:
            try:
                yield ':'.join(proxy.xpath('./td/text()')[0:2])
            except Exception as e:
                pass


if __name__ == "__main__":
    print(list(RawProxyGetter.proxy_jiangxianli()))
    print(list(RawProxyGetter.proxy_ip3366()))
    print(list(RawProxyGetter.proxy_kuaidaili()))
    print(list(RawProxyGetter.proxy_xicidaili()))
