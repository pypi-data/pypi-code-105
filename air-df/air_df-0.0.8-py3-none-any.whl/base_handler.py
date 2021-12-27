import json
import traceback
import tornado.web
import tornado.httpserver
import tornado.ioloop
from tornado.web import RequestHandler


def tornado_server(route_list, settings=None, port=8888):
    if not settings:
        settings = {
            'template_path': 'templates',
            'static_path': 'static',
            'cookie_secret': 'cookie_secret',
            'debug': False
        }
    app = tornado.web.Application(route_list, **settings)
    server = tornado.httpserver.HTTPServer(app)
    server.listen(port=port)
    print('Tornado server run at http://127.0.0.1:{}'.format(port))
    tornado.ioloop.IOLoop.instance().start()


class WBaseHandler(RequestHandler):
    api_name = 'WBaseHandler'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = json.loads(self.request.body) if self.request.body else {}

    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Credentials', 'false')
        self.set_header('Access-Control-Allow-Origin', '*')
        self.set_header('Access-Control-Allow-Headers', '*')
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, PUT, DELETE, OPTIONS')
        self.set_header('Content-Type', '*')

    def options(self):
        pass
        self.set_status(200)
        self.finish()

    def get(self, *args, **kwargs):
        pass

    def post(self, *args, **kwargs):
        pass

    def delete(self, *args, **kwargs):
        pass

    def put(self, *args, **kwargs):
        pass

    @staticmethod
    def check_params(params=None):
        """
        传入参数检查
        :param params: 必填参数列表
        :return: 有一个为空则返回error_msg
        """

        def _inner(func):
            def inner(obj, *args, **kwargs):
                if params:
                    missing_params = []
                    for param in params:
                        if not obj.data.get(param):
                            missing_params.append(param)
                    if missing_params:
                        WBaseHandler.make_reponse(obj, msg='missing params {}'.format(','.join(missing_params)))
                        return
                try:
                    results = func(obj, *args, **kwargs)
                except:
                    ex_msg = traceback.format_exc()
                    WBaseHandler.make_reponse(obj, msg=ex_msg)
                    return
                if results:
                    WBaseHandler.make_reponse(obj, code=1, msg='success', data=results)
                else:
                    WBaseHandler.make_reponse(obj, msg='data not found!')

            return inner

        return _inner

    @staticmethod
    def make_reponse(obj, code=0, msg='failed', **kwargs):
        res = {
            'code': code,
            'msg': msg,
        }
        res.update(kwargs)
        res = json.dumps(res)
        obj.write(res)
