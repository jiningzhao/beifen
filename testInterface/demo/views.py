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
        self.url1 = settings.URL_BEFORE
        self.url2 = settings.URL_AFTER
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 '
                          '(KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
        }

    def doc_list(self):
        for no in ReadDoc().readdoc():
            no1 = copy.deepcopy(no)
            result1 = self.base_interface(no, self.url1)
            result2 = self.base_interface(no1, self.url2)
            self.diff(result1, result2, no)

    def diff(self, old, new, no):
        if type(old['value']) == dict and type(new['value']) == dict:
            old_key_list = [key for key in old['value']]
            new_key_list = [key for key in new['value']]
            old_exception = [key for key in old_key_list if key not in new_key_list]
            new_exception = [key for key in new_key_list if key not in old_key_list]
            try:
                assert old_exception == new_exception
            except AssertionError as e:
                logger.warning("—————————————value键差异性—————————————————————————")
                logger.warning(f"InterfaceName:{no.get('name')}")
                logger.warning(f'{self.url1}中不同字段为{old_exception}')
                logger.warning(f'{self.url2}中不同字段为{new_exception}')
            for i in old['value']:
                try:
                    assert old['value'][i] == new['value'][i]
                except AssertionError as e:
                    logger.warning("++++++++++++++++++++value值差异性+++++++++++++++++++")
                    logger.warning(f"KEY:{i}")
                    logger.warning(f"InterfaceName:{no.get('name')}")
                    logger.warning(f"{self.url1} : {old['value'][i]}")
                    logger.warning(f"{self.url2} : {new['value'][i]}")
        elif type(old['value']) == str and type(new['value']) == str:
            try:
                assert old['value'] == new['value']
            except AssertionError as e:
                logger.warning(f"************value差异性*****************")
                logger.warning(f"KEY:value")
                logger.warning(f"InterfaceName:{no.get('name')}")
                logger.warning(f"{self.url1} : {old['value']}")
                logger.warning(f"{self.url2} : {new['value']}")
        else:
            logger.warning("************value差异性*****************")
            logger.warning(f"InterfaceName:{no.get('name')}")
            logger.warning(f"{self.url1} : {old['value']}")
            logger.warning(f"{self.url2} : {new['value']}")

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
                # header['token'] = cache.get(url + 'token').decode()
                header['token'] = cache.get(url + 'token')
            except Exception as e:
                logger.warning('redis中不存在token', e)

        param = Sign(ParamFix(data, settings.APPKEY, no.get('name')).param(),
                     settings.SECRET).get_param()

        result = InterfaceRequests(url + no.get('path'), param, header).doc_interface().json()
        if no.get('name') == 'passport.login.security':
            try:
                code = result['value'].split('cncode=')[1]
                cache.set(url + 'code', code, settings.REDIS_TIMEOUT)
            except AttributeError as e:
                logger.warning(url, result, e)

        elif no.get('name') == 'passport.userinfo.bycode':
            try:
                token = result.get('value').get('token')
                cache.set(url + 'token', token, settings.REDIS_TIMEOUT)
            except AttributeError as e:
                logger.warning(result, e)
        else:
            pass
        return result


def haha(a):
    return RunAllCase().doc_list()
