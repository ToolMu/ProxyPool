import time

from apscheduler.schedulers.background import BackgroundScheduler

from src.manager.raw_manager import ProductionManager
from src.manager.refresh_manager import RefreshManager
from src.utils.log_handler import Logger


class ProxyRefreshScheduler:

    @staticmethod
    def run():
        proxy_get_scheduler = BackgroundScheduler()
        proxy_get_scheduler.add_job(ProxyRefreshScheduler._run, 'interval', minutes=3)
        proxy_get_scheduler.start()

        while True:
            time.sleep(5)

    @staticmethod
    def _run():
        proxy_data, proxy_channel = RefreshManager().refresh()
        ProductionManager().production(proxy_data, proxy_channel)
        Logger("ProxyPool").get_log().info("[ProxyRefreshScheduler] Refresh Proxy And Add To The Production Queue")


if __name__ == '__main__':
    ProxyRefreshScheduler.run()
