# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import configparser

config = configparser.ConfigParser()
config.read('config.conf',encoding="utf-8-sig")

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

播放链接：'''+ player_url +'''

分享【京东商品链接】或者【淘口令】
精准查询商品优惠券和返利信息！

优惠券使用教程：
'''+config.get('URL', 'course')+'''
免费看电影方法：
'''+config.get('URL', 'movie')+'''
邀请好友得返利说明：
'''+config.get('URL', 'lnvit')+'''
                        '''
                return text

    def getGroupMovie(self, msg):
        soup_xml = BeautifulSoup(msg['Content'], 'lxml')
        xml_info = soup_xml.select('appname')
        # 定义视频网站
        shipin = ['腾讯视频', '爱奇艺', '优酷视频', '芒果 TV']

        for item in shipin:
            if item == xml_info[0].string:
                player_url = 'http://164dyw.duapp.com/youku/apiget.php?url=%s' % msg['Url']
                text = '''
一一一一 视频信息 一一一一

播放链接：'''+ player_url +'''

分享【京东商品链接】或者【淘口令】
精准查询商品优惠券和返利信息！

优惠券使用教程：
'''+config.get('URL', 'course')+'''
免费看电影方法：
'''+config.get('URL', 'movie')+'''
                        '''
                return text