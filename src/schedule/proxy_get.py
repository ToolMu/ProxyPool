import time

from apscheduler.schedulers.background import BackgroundScheduler

from src.manager.raw_manager import ProductionManager, GetterManager


class ProxyGetScheduler:

    @staticmethod
    def run():
        proxy_get_scheduler = BackgroundScheduler()
        proxy_get_scheduler.add_job(ProxyGetScheduler._run, 'interval', minutes=2)
        proxy_get_scheduler.start()

        while True:
            time.sleep(5)

    @staticmethod
    def _run():
        for _ in range(4):
            proxy_data = GetterManager().random_proxy_get()
            ProductionManager().production(proxy_data)


if __name__ == '__main__':
    ProxyGetScheduler.run()
