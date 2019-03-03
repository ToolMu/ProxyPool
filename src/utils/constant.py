import os


REQUESTS_TIMEOUT = 10

REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
REDIS_PASSWORD = None

REDIS_PRODUCTION_CHANNEL = "proxy:production:channel"

VALID_URL = "http://httpbin.org/ip"
THREADNUM = 4

MYSQL_HOME = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWD = "123456"
MYSQL_PROXY_CHANNEL = "proxypool"

REFRESH_NUM = 20

ITEM_ROOT = os.path.join(os.path.dirname(os.path.abspath(__name__)), "../../")
LOG_DIR = os.path.join(ITEM_ROOT, 'log/')
