import time


class ParamFix:

    def __init__(self, data, appkey, interfacename):  # appkey取配置文件
        self.data = data
        self.appkey = appkey
        self.interfacename = interfacename

    def param(self):
        return {
            "name": self.interfacename,
            "version": "",
            "app_key": self.appkey,
            "data": self.data,
            "timestamp": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime()),
            "format": "json"
        }
