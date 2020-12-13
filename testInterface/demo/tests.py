from django.test import TestCase
from django.contrib import admin

# Register your models here.

from .factory.interface import InterfaceRequests
from .factory.bemd5 import Md5
from .factory.param import ParamFix
from .factory.sign import Sign
import logging
from django.conf import settings
from .readDoc import ReadDoc
import copy
from django.core.cache import cache

header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}
logger = logging.getLogger('django')  # 刚才在setting.py中配置的logger


class RunAllCase:
    def __init__(self):
        """
        初始化参数
        """
        self.url1 = settings.URL_BEFORE
        self.url2 = settings.URL_AFTER
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }
    """
    拿到两次的调用结果，调用函数进行结果比对
    """
    def doc_list(self):
        for no in ReadDoc('passport').readdoc():
            no1 = copy.deepcopy(no)
            result1 = self.base_interface(no, self.url1)
            result2 = self.base_interface(no1, self.url2)
            self.diff(result1, result2, no)
    """
    对比两个结果，并输出不同之处
    """
    def diff(self, old, new, no):
        try:
            if type(old['value']) == dict and type(new['value']) == dict:
                old_key_list = [key for key in old['value']]
                new_key_list = [key for key in new['value']]
                old_exception = [key for key in old_key_list if key not in new_key_list]
                new_exception = [key for key in new_key_list if key not in old_key_list]
                try:
                    assert old_exception == new_exception
                except AssertionError as e:
                    logger.warning("—————————————value键差异性—————————————————————————")
                    self.logging_print(old, new, no)
                for i in old['value']:
                    try:
                        assert old['value'][i] == new['value'][i]
                    except AssertionError as e:
                        logger.warning("++++++++++++++++++++value值差异性+++++++++++++++++++")
                        logger.warning(f"KEY:{i}")
                        logger.warning(f"InterfaceName:{no.get('name')}")
                        logger.warning(f"InterfaceName:{no.get('detail')}")
                        logger.warning(f"{self.url1} : {old['value'][i]}")
                        logger.warning(f"{self.url2} : {new['value'][i]}")
                        # self.logging_print(old, new, no)
            else:
                try:
                    assert old['value'] == new['value']
                except AssertionError as e:
                    logger.warning(f"************value差异性*****************")
                    self.logging_print(old, new, no)
        except Exception as e:
            logger.critical(e)
            logger.critical(no.get('name'))
    """
    封装打印方法
    """
    def logging_print(self, old, new, no):
        logger.warning(f"InterfaceName:{no.get('name')}")
        logger.warning(f"InterfaceName:{no.get('detail')}")
        logger.warning(f"{self.url1} : {old['value']}")
        logger.warning(f"{self.url2} : {new['value']}")

    """
    调用接口
    """
    @staticmethod
    def base_interface(no, url):

        data = no.get('data')

        if "password" in data:
            data["password"] = Md5().md5(data["password"])
            header['token'] = ''
        elif "code" in data:
            try:
                # data["code"] = cache.get(url + 'code').decode()
                data["code"] = cache.get(url + 'code')
                header['token'] = ''
            except Exception as e:
                logger.warning("redis中不存在对应的code", e)
        else:
            try:
                header['token'] = cache.get(url + 'token')
            except Exception as e:
                logger.warning('redis中不存在token', e)
        """
        调用签名算法给入参签名
        """
        param = Sign(ParamFix(data, settings.APPKEY, no.get('name')).param(),
                     settings.SECRET).get_param()

        """
        拿到接口的返回值
        """
        response = InterfaceRequests(url + no.get('path'), param, header).doc_interface()
        if response.status_code != 200:
            logger.error(f"{url}:{no.get('detail')},接口返回状态不为200！")
        else:
            result = response.json()

            """
            判断接口是否是登陆接口，需要在redis中存入code值来供下一个接口使用
            拿到token并存到redis中
            """
            if no.get('name') == 'passport.login.security':
                try:
                    code = result['value'].split('cncode=')[1]
                    cache.set(url + 'code', code, settings.REDIS_TIMEOUT)
                except AttributeError as e:
                    logger.warning(url, result, e)
            elif no.get('name') == 'passport.userinfo.bycode':
                try:
                    token = result.get('value').get('token')
                    # cache.set(url + 'token', token, settings.REDIS_TIMEOUT)
                    cache.set(url + 'token', token, None)
                except AttributeError as e:
                    logger.warning(result, e)
            else:
                pass
            return result

# Create your tests here.
