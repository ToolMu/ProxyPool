import os

from src.utils.config import Config
from config_path import CONF_DIR

file_name = os.path.join(CONF_DIR, 'base.yaml')

config = Config.from_yaml(file_name)

REQUESTS_TIMEOUT = config['request.timeout']

REDIS_HOST = config['redis.host']
REDIS_PORT = config['redis.port']
REDIS_PASSWORD = config['redis.passwd']

REDIS_PRODUCTION_CHANNEL = config['redis.production_channel']

VALID_URL = config['valid.url']

THREADNUM = config['threadpool.num']

MYSQL_HOME = config["mysql.host"]
MYSQL_USER = config["mysql.user"]
MYSQL_PASSWD = config["mysql.passwd"]
MYSQL_PROXY_CHANNEL = config["mysql.proxy_channel"]

REFRESH_NUM = config["refresh.num"]

MAX_IP = config["refresh.max_ip"]
