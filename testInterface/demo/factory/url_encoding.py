from urllib.parse import quote


class UrlEncoding:
    @staticmethod
    def url_encoding(data) -> str:
        # 1.将data转换为字符串
        string_data = str(data)

        # 2.把字符串转换为bytes类型
        string_data = string_data.encode("utf-8")

        # 3.最后进行url编码
        url_data = quote(string_data)

        return url_data
