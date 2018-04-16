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
import configparser
from threading import Thread
from libs.mediaJd import MediaJd
from libs.mysql import ConnectMysql
from bs4 import BeautifulSoup
from bottle import template
from libs.groupMessage import FormData

mjd = MediaJd()
mjd.login()
fm = FormData()
config = configparser.ConfigParser()
config.read('config.conf',encoding="utf-8-sig")


class WxBot(object):

    def __init__(self):
        fm.groupMessages()
        print('run.....')
        self.run()

    def run(self):
        sysstr = platform.system()

        if (sysstr == "Linux") or (sysstr == "Darwin"):
            itchat.auto_login(enableCmdQR=2, hotReload=True, statusStorageDir='peng.pkl')
        else:
            itchat.auto_login(True, statusStorageDir='groupMessages.pkl', enableCmdQR=True)
        itchat.run()

if __name__ == '__main__':
    mi = WxBot()
