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
from threading import Thread
from libs.mediaJd import MediaJd
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
movie = SharMovie()
tm = TextMessage()
fm = FormData()
ort = Orther()

def text_reply(msg, good_url):
    print(11)
    mjd.getJd(msg, good_url)

def check_if_is_tb_link(msg):
    if msg['Type'] == 'Sharing':  # vip 电影
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


def check_if_is_group(msg):
    if msg['Type'] == 'Sharing':
        htm = re.findall(r"<appname>.*?</appname>", msg['Content'])

        if htm:
            soup_xml = BeautifulSoup(msg['Content'], 'lxml')
            xml_info = soup_xml.select('appname')
            if xml_info[0].string == "京东":
                mjd.getGroupJd(msg, msg['Url'])
                return
            else:
                text = movie.getGroupMovie(msg)
                itchat.send(text, msg['FromUserName'])
                return

    elif msg['Type'] == 'Text':
        tm.getGroupText(msg)

class WxBot(object):

    def __init__(self):
        fm.groupMessages()
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

分享【京东商品链接】
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
            itchat.auto_login(enableCmdQR=2, hotReload=True, statusStorageDir='jd.pkl')
        else:
            itchat.auto_login(True, statusStorageDir='jd.pkl')
        itchat.run()

if __name__ == '__main__':
    mi = WxBot()
