from multiprocessing import Process

from src.manager.valid_manager import ValidManager
from src.schedule.proxy_get import ProxyGetScheduler
from src.schedule.proxy_refresh import ProxyRefreshScheduler
from src.api.proxy_api import run as api_run


def valid():
    ValidManager().consumption()


def main():
    processes = []

    processes.append(Process(target=ProxyGetScheduler.run, name="proxy_pool_get"))
    processes.append(Process(target=valid, name="proxy_pool_valid"))
    processes.append(Process(target=ProxyRefreshScheduler.run, name="proxy_pool_refresh"))
    processes.append(Process(target=api_run, name="proxy_pool_web_api"))

    for item in processes:
        item.daemon = True
        item.start()

    for item in processes:
        item.join()


if __name__ == '__main__':
    main()
