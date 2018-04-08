# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

class SharMovie(object):
    def __init__(self):
        pass

    def getMovie(self, msg):
        soup_xml = BeautifulSoup(msg['Content'], 'lxml')
        xml_info = soup_xml.select('appname')
        # 定义视频网站
        shipin = ['腾讯视频', '爱奇艺', '优酷视频', '芒果 TV']

        for item in shipin:
            if item == xml_info[0].string:
                player_url = 'http://164dyw.duapp.com/youku/apiget.php?url=%s' % msg['Url']
                text = '''
一一一一 视频信息 一一一一

播放链接：%s

分享【京东商品链接】或者【淘口令】
精准查询商品优惠券和返利信息！

优惠券使用教程：
http://t.cn/RnAKqWW
免费看电影方法：
http://t.cn/RnAKMul
邀请码好友得返利：
http://t.cn/RnAKafe
                        ''' % (player_url)
                return text

        error_info = '''
一一一一 视频信息 一一一一

抱歉，没找到你想要的视频！

优惠券使用教程：
http://t.cn/RnAKqWW
免费看电影方法：
http://t.cn/RnAKMul
邀请码好友得返利：
http://t.cn/RnAKafe
                    '''
        return error_info
