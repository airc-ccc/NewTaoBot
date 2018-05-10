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
import configparser
from libs import utils
from urllib.parse import quote
from itchat.content import *
from threading import Thread
from libs.mysql import ConnectMysql
from bs4 import BeautifulSoup
from bottle import template
from libs.movie import SharMovie
from libs.tuling import tuling

logger = utils.init_logger()

movie = SharMovie()

config = configparser.ConfigParser()
config.read('config.conf',encoding="utf-8-sig")

class Orther(object):



        # 创建用户账户

    def create_user_info(self, msg, lnivt_code=0, tool=False, wxid=0, sourcname=0):
        cm = ConnectMysql()

        if tool == False:
            res = itchat.search_friends(userName=msg['FromUserName'])
        else:
            res = itchat.search_friends(userName=msg['RecommendInfo']['UserName'])


        bot_info = itchat.search_friends(userName=msg['ToUserName'])

        select = "SELECT * FROM taojin_user_info WHERE wx_number='" + res['NickName'] + "' AND wx_bot='"+ bot_info['NickName'] +"'"

        is_ext = cm.ExecQuery(select)

        if is_ext == None:
            return

        if lnivt_code == 0:
            sql = "INSERT INTO taojin_user_info(wx_bot, wx_number, sex, nickname, lnivt_code, withdrawals_amount, lnivter, create_time) VALUES('"+ bot_info['NickName'] +"', '" + \
                  res['NickName'] + "', '" + str(res['Sex']) + "', '" + res['NickName'] + "', '" + str(
                wxid) + "', '0.3', '" + str(lnivt_code) + "', '" + str(round(time.time())) + "');"

            insert_res = cm.ExecNonQuery(sql)
            # 日志参数
            args = {
                'wx_bot': bot_info['NickName'],
                'username': res['NickName'],
                'rebate_amount': 0.3,
                'type': 1,
                'create_time': time.time()
            }
            # 写入返利日志
            cm.InsertRebateLog(args)
            return
        else:
            lnivt_2_info = itchat.search_friends(nickName=sourcname)

            lnivter_sql = "SELECT * FROM taojin_user_info WHERE lnivt_code='" + lnivt_code + "' AND wx_bot='"+ bot_info['NickName'] +"' LIMIT 1;"
            # 获取邀请人信息
            lnivt_info = cm.ExecQuery(lnivter_sql)
            if lnivt_info == ():
                lnivter_sql = "SELECT * FROM taojin_user_info WHERE nickname='" + sourcname + "' AND wx_bot='"+ bot_info['NickName'] +"' LIMIT 1;"
                # 获取邀请人信息
                lnivt_info = cm.ExecQuery(lnivter_sql)

                if lnivt_info != ():
                    u_sql = "UPDATE taojin_user_info SET lnivt_code='" + lnivt_code + "' WHERE nickname='" + sourcname + "' AND wx_bot='"+ bot_info['NickName'] +"';"
                    # 修改邀请人wxid
                    cm.ExecNonQuery(u_sql)

            # 有邀请人时，插入用户信息，并奖励邀请人
            sql = "INSERT INTO taojin_user_info(wx_bot, wx_number, sex, nickname, lnivt_code, withdrawals_amount, lnivter, create_time) VALUES('"+ bot_info['NickName'] +"', '" + \
                  res['NickName'] + "', '" + str(res['Sex']) + "', '" + res['NickName'] + "', '" + str(
                wxid) + "', '0.3', '" + str(lnivt_code) + "', '" + str(round(time.time())) + "');"

            # 给邀请人余额加0.3元奖励
            jianli = round(float(lnivt_info[0][9]) + 0.3, 2)

            friends_num = int(lnivt_info[0][20]) + 1

            cm.ExecNonQuery("UPDATE taojin_user_info SET withdrawals_amount='" + str(
                jianli) + "', friends_number='" + str(friends_num) + "'  WHERE lnivt_code='" + lnivt_code + "' AND wx_bot='"+ bot_info['NickName'] +"';")

            cm.ExecNonQuery(sql)

            # 日志参数
            args = {
                'wx_bot': bot_info['NickName'],
                'username': res['NickName'],
                'rebate_amount': 0.3,
                'type': 1,
                'create_time': time.time()
            }

            args2 = {
                'wx_bot': bot_info['NickName'],
                'username': lnivt_info[0][2],
                'rebate_amount': 0.3,
                'type': 2,
                'create_time': time.time()
            }

            # 写入返利日志
            cm.InsertRebateLog(args)
            cm.InsertRebateLog(args2)
            user_sql = "SELECT * FROM taojin_user_info WHERE wx_number='" + res['NickName'] + "' AND wx_bot='"+ bot_info['NickName'] +"';"
            user_info = cm.ExecQuery(user_sql)
            lnivt_text = '''
一一一一系统消息一一一一

您的好友【%s】已邀请成功！

0.3元奖励金已到账
您将永久获得该好友永久购物返利佣金提成

邀请好友得返利说明：
'''+config.get('URL', 'lnvit')+'''
            ''' % (user_info[0][4])

            cm.Close()
            itchat.send(lnivt_text, lnivt_2_info[0]['UserName'])

        # 使用邀请码创建账户, 或绑定邀请人

    def lnivt_user(self, msg):
        cm = ConnectMysql()

        res = itchat.search_friends(userName=msg['FromUserName'])

        check_user_sql = "SELECT * FROM taojin_user_info WHERE wx_number='" + str(res['NickName']) + "';"
        check_user_res = cm.ExecQuery(check_user_sql)

        # 判断是否已经有个人账户，没有去创建
        if len(check_user_res) < 1:
            cm.Close()
            create_user_info(msg, msg['Text'])
        else:
            # 定义SQL语句 查询用户是否已经存在邀请人
            # 判断是否已经有邀请人了
            if check_user_res and check_user_res[0][16] != 0:
                cm.Close()
                gg_text = '''
一一一一系统消息一一一一

好友关系绑定失败！

分享【京东商品链接】或者【淘口令】
精准查询商品优惠券和返利信息！

优惠券使用教程：
'''+config.get('URL', 'course')+'''
免费看电影方法：
'''+config.get('URL', 'movie')+'''
邀请好友得返利说明：
'''+config.get('URL', 'lnvit')+'''
        `                   '''
                itchat.send(gg_text, msg['FromUserName'])
                return
            elif int(msg['Text']) == int(check_user_res[0][4]):
                cm.Close()
                gg_text = '''
一一一一系统消息一一一一

好友关系绑定失败！

分享【京东商品链接】或者【淘口令】
精准查询商品优惠券和返利信息！

优惠券使用教程：
'''+config.get('URL', 'course')+'''
免费看电影方法：
'''+config.get('URL', 'movie')+'''
邀请好友得返利说明：
'''+config.get('URL', 'lnvit')+'''
        `                   '''
                itchat.send(gg_text, msg['FromUserName'])
                return

            inivt_code_sql = "SELECT * FROM taojin_user_info WHERE lnivt_code='" + str(msg['Text']) + "';"
            inivt_code_res = cm.ExecQuery(inivt_code_sql)

            # 判断邀请人是否真实
            if len(inivt_code_res) < 1:
                cm.Close()
                gg_text = '''
一一一一系统消息一一一一

账户创建失败：邀请码无效，
请检查邀请码并重新发送！
                          '''
                itchat.send(gg_text, msg['FromUserName'])
                return

            # 绑定邀请人
            add_lnivt_sql = "UPDATE taojin_user_info SET lnivter='" + str(msg['Text']) + "' WHERE wx_number='" + \
                            res[
                                'NickName'] + "';"

            add_res = cm.ExecNonQuery(add_lnivt_sql)

            lnivter_sql = "SELECT * FROM taojin_user_info WHERE lnivt_code='" + str(msg['Text']) + "' LIMIT 1;"

            # 获取邀请人信息
            lnivt_info = cm.ExecQuery(lnivter_sql)

            # 给邀请人余额加0.3元奖励
            jianli = round(float(lnivt_info[0][8]) + 0.3, 2)

            friends_num = int(lnivt_info[0][19]) + 1

            lnivt_res = cm.ExecNonQuery(
                "UPDATE taojin_user_info SET withdrawals_amount='" + str(jianli) + "', friends_number='" + str(
                    friends_num) + "' WHERE lnivt_code='" + str(msg['Text']) + "';")

            args = {
                'username': lnivt_info[0][1],
                'rebate_amount': 0.3,
                'type': 2,
                'create_time': time.time()
            }

            # 写入返利日志
            cm.InsertRebateLog(args)

            if add_res:
                cm.Close()
                text = '''
一一一一 系统消息 一一一一

账户创建成功！0.3元奖励金已到账
回复【个人信息】查看账户详情
回复【帮助】查看指令说明

分享【京东商品链接】或者【淘口令】
精准查询商品优惠券和返利信息！

优惠券使用教程：
'''+config.get('URL', 'course')+'''
免费看电影方法：
'''+config.get('URL', 'movie')+'''
邀请好友得返利说明：
'''+config.get('URL', 'lnvit')+'''
                        ''' % (check_user_res[0][4])

                lnivt_text = '''
一一一一系统消息一一一一

您的好友【%s】已邀请成功！

0.3元奖励金已到账
您将永久获得该好友永久购物返利佣金提成

邀请好友得返利说明：
'''+config.get('URL', 'lnvit')+'''
                ''' % (check_user_res[0][3])
                itchat.send(text, msg['FromUserName'])
                itchat.send(lnivt_text, lnivt_info[0][1])
            else:
                cm.Close()
                itchat.send('添加邀请人失败！请重试！', msg['FromUserName'])

        # 判断用户是否有个人账户

    def ishaveuserinfo(self, msg):
        cm = ConnectMysql()

        res = itchat.search_friends(userName=msg['FromUserName'])
        bot_info = itchat.search_friends(userName=msg['ToUserName'])
        check_user_sql = "SELECT * FROM taojin_user_info WHERE wx_number='" + str(res['NickName']) + "' AND wx_bot='"+ bot_info['NickName'] +"';"
        check_user_res = cm.ExecQuery(check_user_sql)
        # 判断是否已经有个人账户，没有去创建
        if len(check_user_res) < 1:
            cm.Close()
            send_text = '''
一一一一 个人信息 一一一一

你还没创建个人账户哦！

回复【邀请码】创建个人账户哦!
还可以领取现金红包哦！

优惠券使用教程：
'''+config.get('URL', 'course')+'''
                        '''
            return {"res": "not_info", "text": send_text}

        return {"res": "have_info"}
