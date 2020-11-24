import os
import configparser as cparser


class Conf:
    def __init__(self):
        # 定位当前脚本所在位置的上级
        base_dir = str(os.path.dirname(__file__))
        # 对文件路径进行格式处理
        base_dir = base_dir.replace("\\", "/")
        # 定位到api_config.ini文件
        file_path = base_dir + "/url.ini"

        # ConfigParser功能——读取写入配置文件
        self.cf = cparser.ConfigParser()
        # read(filename)——直接读取文件内容
        self.cf.read(file_path)

    def url(self):
        url1 = self.cf.get("url", "url1")
        url2 = self.cf.get("url", "url2")
        appkey = self.cf.get("url", "appkey")
        secret = self.cf.get("url", "secret")

        return {'url1': url1, 'url2': url2, 'appkey': appkey, 'secret': secret}
