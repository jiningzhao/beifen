# encoding: utf-8
"""
开发者：赵吉宁
脚本功能：接口登录
时间：2019-10-23
"""

import hashlib
from urllib.parse import quote
from Conf.config import Conf


class Sign:
    def __init__(self, param):
        self.url, self.app_key, self.secret = Conf().api_conf()
        self.param = self.param_fix(param)

    # 处理入参的函数
    def param_fix(self, param):
        data = param['data']
        if 'password' in data:
            password = self.md5(data['password'])
            data['password'] = password
        param['data'] = self.url_encoding(data)
        param['sign'] = self.sign(param)

        return param

    def sign(self, param):
        param_keys = sorted(list(param.keys()), reverse=False)
        list_param = [self.secret]
        for param_key in param_keys:
            list_param.append(param_key)
            list_param.append(param[param_key])
        list_param.append(self.secret)
        string_sign = ''.join(list_param)

        return self.md5(string_sign)

    @staticmethod
    def url_encoding(data):
        string_data = str(data)
        string_data = string_data.encode("utf-8")
        url_data = quote(string_data)

        return url_data

    @staticmethod
    def md5(data):
        m = hashlib.md5()
        m.update(data.encode("utf-8"))
        md = m.hexdigest().upper()

        return md
