import time

from apscheduler.schedulers.background import BackgroundScheduler

from src.manager.raw_manager import ProductionManager, GetterManager
from src.utils.log_handler import Logger


class ProxyGetScheduler:

    @staticmethod
    def run():
        proxy_get_scheduler = BackgroundScheduler()
        proxy_get_scheduler.add_job(ProxyGetScheduler._run, 'interval', minutes=3)
        proxy_get_scheduler.start()

        while True:
            time.sleep(5)

    @staticmethod
    def _run():
        for _ in range(4):
            proxy_data = GetterManager().random_proxy_get()
            ProductionManager().production(proxy_data)
        Logger("ProxyPool").get_log().info("[ProxyGetScheduler] Get Proxy And Add To The Production Queue")


if __name__ == '__main__':
    ProxyGetScheduler.run()
