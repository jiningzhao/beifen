from interface import InterfaceRequests
from bemd5 import Md5
from param import ParamFix
from sign import Sign
import logging
from config.readConfig import Conf
from doc.readDoc import ReadDoc
import redis

r = redis.Redis(host='0.0.0.0', port=6379)
url1 = Conf().url().get('url1')
url2 = Conf().url().get('url2')
header = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 '
                  '(KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36'
}

if __name__ == "__main__":
    for no in ReadDoc().readdoc():
        print(no)
        data = no.get('data')
        if "password" in data:
            data["password"] = Md5().md5(data["password"])
        interfacename = no.get('name')
        param = Sign(ParamFix(data, Conf().url().get('appkey'), interfacename).param(),
                     Conf().url().get('secret')).get_param()


        result1 = InterfaceRequests(url1 + no.get('path'), param, header).doc_interface().json()
        result2 = InterfaceRequests(url2 + no.get('path'), param, header).doc_interface().json()
        if interfacename == 'passport.login.security':
            code_1 = result1['value'].split('cncode=')[1]
            code_2 = result2['value'].split('cncode=')[1]
            r.set('code_1', code_1, px=6000000)
            r.set('code_2', code_2, px=6000000)
        for i in result1:
            try:
                assert result1[i] == result2[i]
            except Exception as e:
                logging.warning(f'url:{url1}: {i} : {result1[i]}')
                logging.warning(f'url:{url2}: {i} : {result2[i]}')
