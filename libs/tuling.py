# -*-coding: UTF-8-*-

import json
import requests

class tuling(object):

    def getTulingText(self, url):
        page = requests.get(url)
        text = page.text
        return text

    def tuling(self, msg):
        print('图灵')
        # 图灵Key
        key = '069f41c6c6924260b9d1bbdc24affd07'
        api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='

        request = api + msg['Text']
        response = self.getTulingText(request)
        dic_json = json.loads(response)
        return dic_json['text']