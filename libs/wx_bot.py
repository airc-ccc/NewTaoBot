# -*-coding: UTF-8-*-

from __future__ import unicode_literals
import itchat
import re
import time
import json
import platform
import requests
import threading
import traceback
import random
import webbrowser
from libs import utils
from urllib.parse import quote
from itchat.content import *
from libs.mediaJd import MediaJd
from threading import Thread
from libs.alimama import Alimama
from libs.mysql import ConnectMysql
from bs4 import BeautifulSoup
from bottle import template
from libs.groupMessage import FormData
from libs.movie import SharMovie
from libs.tuling import tuling
from libs.orther import Orther
from libs.textMessage import TextMessage

logger = utils.init_logger()

mjd = MediaJd()
mjd.login()
al = Alimama(logger)
al.login()
movie = SharMovie()
tm = TextMessage()
fm = FormData()
ort = Orther()

"""
    
    [["t", "226ef818793c9a6696f1ad1a14549b55"], ["cookie2", "1e099371140b4c60bfc13f085295d7d8"], ["v", "0"], ["_tb_token_", "e3a5e69e6d8ee"], ["alimamapwag", "TW96aWxsYS81LjAgKFdpbmRvd3MgTlQgMTAuMDsgV2luNjQ7IHg2NDsgcnY6NTkuMCkgR2Vja28vMjAxMDAxMDEgRmlyZWZveC81OS4w"], ["cookie32", "6d50a6f9ad98f2c0f0a1978a4bf9cd5a"], ["alimamapw", "QhRcX15tCANSAwIEAQ4IUwIBDFZXVQQHCwEFBFZUAQheBQZSUAY%3D"], ["cookie31", "MjE4Njc3MDYsd3BobGosZ2VuZXI0MTJAc2luYS5jb20sVEI%3D"], ["login", "W5iHLLyFOGW7aA%3D%3D"], ["cna", "2R5RE//Gs3wCAWU2iTPVVSRB"], ["isg", "BFJSCT9NXCeIIKDbfOxDPs39oBs0Y1b9yLd6ghyrfoXwL_IpBPOmDVjNmwMTRM6V"], ["apush86b7c0cd604ee7fb04c27a04565ab3a7", "%7B%22ts%22%3A1523200250579%2C%22parentId%22%3A1523200250570%7D"]]

"""


def text_reply(msg, good_url):
    print(11)
    mjd.getJd(msg, good_url)

# 检查是否是淘宝链接
def check_if_is_tb_link(msg):
    if re.search(r'【.*】', msg['Text']) and (
            u'打开👉手机淘宝👈' in msg['Text'] or u'打开👉天猫APP👈' in msg['Text'] or u'打开👉手淘👈' in msg['Text']):
        al.getTao(msg)

    elif msg['Type'] == 'Sharing':  # vip 电影
        res = ort.ishaveuserinfo(msg)
        if res['res'] == 'not_info':
            ort.create_user_info(msg, 0, tool=False)

        htm = re.findall(r"<appname>.*?</appname>", msg['Content'])

        if htm:
            soup_xml = BeautifulSoup(msg['Content'], 'lxml')
            xml_info = soup_xml.select('appname')
            if xml_info[0].string == "京东":
                text_reply(msg, msg['Url'])
                return
            else:
                text = movie.getMovie(msg)
                itchat.send(text, msg['FromUserName'])
                return

        
    elif msg['Type'] == 'Text':  # 关键字查询信息
        tm.getText(msg)


# 检查是否是淘宝链接
def check_if_is_group(msg):
    if re.search(r'【.*】', msg['Text']) and (
            u'打开👉手机淘宝👈' in msg['Text'] or u'打开👉天猫APP👈' in msg['Text'] or u'打开👉手淘👈' in msg['Text']):
        al.getGroupTao(msg)

    elif msg['Type'] == 'Sharing':

        htm = re.findall(r"<appname>.*?</appname>", msg['Content'])

        if htm:
            soup_xml = BeautifulSoup(msg['Content'], 'lxml')
            xml_info = soup_xml.select('appname')
            if xml_info[0].string == "京东":
                mjd.getGroupJd(msg, msg['Url'])
                return
            else:
                text = movie.getMovie(msg)
                itchat.send(text, msg['FromUserName'])
                return

    elif msg['Type'] == 'Text':
        tm.getGroupText(msg)

class WxBot(object):

    def __init__(self):
        # fm.groupMessages()
        print('run.....')
        self.run()

    # 消息回复(文本类型和分享类型消息)
    @itchat.msg_register(['Text', 'Sharing', 'Card'])
    def text(msg):
        print(msg)
        check_if_is_tb_link(msg)

    # 消息回复(文本类型和分享类型消息) 群聊
    @itchat.msg_register(['Text', 'Sharing'], isGroupChat=True)
    def text(msg):
        print(msg)
        check_if_is_group(msg)

    @itchat.msg_register(FRIENDS)
    def add_friend(msg):
        print(msg)
        itchat.add_friend(**msg['Text'])  # 该操作会自动将新好友的消息录入，不需要重载通讯录

        soup = BeautifulSoup(msg['Content'], 'lxml')

        msg_soup = soup.find('msg')

        sourc = msg_soup.get('sourceusername')
        sourcname = msg_soup.get('sourcenickname')

        user_wxid = msg_soup.get('fromusername')

        print(sourc)
        if sourc == '':
            sourc = 0

        ort.create_user_info(msg, lnivt_code=sourc, tool=True, wxid=user_wxid, sourcname=sourcname)
        text = '''
一一一一 系统消息 一一一一

分享【京东商品链接】或者【淘口令】
精准查询商品优惠券和返利信息！

优惠券使用教程：
http://t.cn/RnAKqWW
免费看电影方法：
http://t.cn/RnAKMul
邀请好友得返利：
http://t.cn/RnAKafe
                '''
        itchat.send_msg(text, msg['RecommendInfo']['UserName'])

    def run(self):
        sysstr = platform.system()

        if (sysstr == "Linux") or (sysstr == "Darwin"):
            itchat.auto_login(enableCmdQR=2, hotReload=True, statusStorageDir='peng.pkl')
        else:
            itchat.auto_login(True)
        itchat.run()

if __name__ == '__main__':
    mi = WxBot()
