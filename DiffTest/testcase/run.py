from interface import InterfaceRequests
from bemd5 import Md5
from param import ParamFix
from sign import Sign
import logging
from config.readConfig import Conf
from doc.readDoc import ReadDoc
import redis
import copy

# 链接本地reids数据库
r = redis.Redis(host='0.0.0.0', port=6379)
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}


class RunAllCase:
    def __init__(self):
        self.url1 = Conf().url().get('url1')
        self.url2 = Conf().url().get('url2')
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
                logging.warning("—————————————value键差异性—————————————————————————")
                logging.warning(f"InterfaceName:{no.get('name')}")
                logging.warning(f'{self.url1}中不同字段为{old_exception}')
                logging.warning(f'{self.url2}中不同字段为{new_exception}')
            for i in old['value']:
                try:
                    assert old['value'][i] == new['value'][i]
                except AssertionError as e:
                    logging.warning("++++++++++++++++++++value值差异性+++++++++++++++++++")
                    logging.warning(f"KEY:{i}")
                    logging.warning(f"InterfaceName:{no.get('name')}")
                    logging.warning(f"{self.url1} : {old['value'][i]}")
                    logging.warning(f"{self.url2} : {new['value'][i]}")
        elif type(old['value']) == str and type(new['value']) == str:
            try:
                assert old['value'] == new['value']
            except AssertionError as e:
                logging.warning(f"************value差异性*****************")
                logging.warning(f"KEY:value")
                logging.warning(f"InterfaceName:{no.get('name')}")
                logging.warning(f"{self.url1} : {old['value']}")
                logging.warning(f"{self.url2} : {new['value']}")
        else:
            logging.warning("************value差异性*****************")
            logging.warning(f"InterfaceName:{no.get('name')}")
            logging.warning(f"{self.url1} : {old['value']}")
            logging.warning(f"{self.url2} : {new['value']}")

    @staticmethod
    def base_interface(no, url):

        data = no.get('data')

        if "password" in data:
            data["password"] = Md5().md5(data["password"])
            header['token'] = ''
        elif "code" in data:
            try:
                data["code"] = r.get(url + 'code').decode()
                header['token'] = ''
            except Exception as e:
                logging.warning("redis中不存在对应的code", e)
        else:
            try:
                header['token'] = r.get(url + 'token').decode()
            except Exception as e:
                logging.warning('redis中不存在token', e)

        param = Sign(ParamFix(data, Conf().url().get('appkey'), no.get('name')).param(),
                     Conf().url().get('secret')).get_param()

        result = InterfaceRequests(url + no.get('path'), param, header).doc_interface().json()
        if no.get('name') == 'passport.login.security':
            try:
                code = result['value'].split('cncode=')[1]
                r.set(url + 'code', code, px=6000000)
            except AttributeError as e:
                logging.warning(url, result, e)

        elif no.get('name') == 'passport.userinfo.bycode':
            try:
                token = result.get('value').get('token')
                r.set(url + 'token', token, px=6000000)
            except AttributeError as e:
                logging.warning(result, e)
        else:
            pass
        return result


if __name__ == "__main__":
    RunAllCase().doc_list()
