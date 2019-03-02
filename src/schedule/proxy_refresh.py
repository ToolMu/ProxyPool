import time

from apscheduler.schedulers.background import BackgroundScheduler

from src.manager.raw_manager import ProductionManager
from src.manager.refresh_manager import RefreshManager


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
        proxy_data = RefreshManager().refresh()
        ProductionManager().production(proxy_data)


if __name__ == '__main__':
    ProxyRefreshScheduler.run()
