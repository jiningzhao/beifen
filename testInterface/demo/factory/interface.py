import requests



class InterfaceRequests:
    def __init__(self, url, data, header):
        self.url = url
        self.data = data
        self.header = header

    def doc_interface(self):
        response = requests.post(self.url, params=self.data, headers=self.header)
        return response
