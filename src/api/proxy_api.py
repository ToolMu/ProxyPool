from flask import Flask
from flask import request, Response, jsonify
from flask.views import MethodView
import pymysql

from src.utils.constant import MYSQL_HOME, MYSQL_USER, MYSQL_PASSWD, MYSQL_PROXY_CHANNEL


app = Flask(__name__)


class JsonResponse(Response):
    @classmethod
    def force_type(cls, response, environ=None):
        if isinstance(response, (dict, list)):
            response = jsonify(response)

        return super(JsonResponse, cls).force_type(response, environ)


app.response_class = JsonResponse


class ProxyIPS(MethodView):

    def get(self):
        get_ip_nums = request.args.get("num", 5)

        _mysql_con = pymysql.connect(MYSQL_HOME, MYSQL_USER, MYSQL_PASSWD, MYSQL_PROXY_CHANNEL)
        _mysql_cursor = _mysql_con.cursor()

        select_sql = "SELECT ip_str FROM proxyip ORDER BY rand(), ip_id LIMIT {}".format(get_ip_nums)
        _mysql_cursor.execute(select_sql)
        proxy_ips = [item[0] for item in _mysql_cursor.fetchall()]

        _mysql_con.close()

        return {'proxy_ips': proxy_ips}


class SigProxyIP(MethodView):

    def get(self):
        _mysql_con = pymysql.connect(MYSQL_HOME, MYSQL_USER, MYSQL_PASSWD, MYSQL_PROXY_CHANNEL)
        _mysql_cursor = _mysql_con.cursor()

        select_sql = "SELECT ip_str FROM proxyip ORDER BY rand(), ip_id LIMIT 1"
        _mysql_cursor.execute(select_sql)
        proxy_ip_str = _mysql_cursor.fetchone()

        _mysql_con.close()

        return {'proxy_ip': proxy_ip_str}

    def delete(self):
        delete_ip_str = request.args.get("proxy")
        if not delete_ip_str:
            return {"status": 40000, "message": "Args Message lose!"}

        _mysql_con = pymysql.connect(MYSQL_HOME, MYSQL_USER, MYSQL_PASSWD, MYSQL_PROXY_CHANNEL)
        _mysql_cursor = _mysql_con.cursor()

        select_sql = "DELETE FROM proxyip WHERE ip_str='{}'".format(delete_ip_str)
        try:
            _mysql_cursor.execute(select_sql)
            _mysql_con.commit()
        except Exception as e:
            _mysql_con.rollback()
            return {"status": 50000, "message": e}
        finally:
            _mysql_con.close()

        return {"status": 20000, "message": "delete success!"}


class ProxyPoolStatus(MethodView):

    def get(self):
        _mysql_con = pymysql.connect(MYSQL_HOME, MYSQL_USER, MYSQL_PASSWD, MYSQL_PROXY_CHANNEL)
        _mysql_cursor = _mysql_con.cursor()

        select_sql = "SELECT count(ip_str) FROM proxyip"
        _mysql_cursor.execute(select_sql)
        ip_numbers = _mysql_cursor.fetchone()

        _mysql_con.close()

        return {'proxy_ip_numbers': ip_numbers[0]}


app.add_url_rule('/proxy_ips', view_func=ProxyIPS.as_view("proxy_ips"))
app.add_url_rule('/proxy_ip', view_func=SigProxyIP.as_view("sig_proxy_ip"))
app.add_url_rule('/proxy_pool_size', view_func=ProxyPoolStatus.as_view("proxy_pool_status"))


def run():
    app.run(host="0.0.0.0", port=8909)


if __name__ == '__main__':
    run()
