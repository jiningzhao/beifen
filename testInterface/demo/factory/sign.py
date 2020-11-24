from .bemd5 import Md5
from .url_encoding import UrlEncoding


class Sign:

    def __init__(self, params, secret):  # secret取配置文件
        self.params = params
        self.secret = secret

    def add_sign(self):
        keys = list(self.params.keys())
        keys.sort()
        strdata = ''
        for key in keys:
            strdata += key + self.params[key]
        return Md5().md5(str(self.secret + strdata + self.secret))

    def get_param(self):
        self.params['data'] = UrlEncoding().url_encoding(self.params['data'])
        self.params['sign'] = self.add_sign()
        return self.params
