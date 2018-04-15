# -*-coding: UTF-8-*-

import itchat
import re
import time
import json
import requests
import random
from libs import utils
import configparser
from urllib.parse import quote
from itchat.content import *
from libs.mediaJd import MediaJd
from libs.alimama import Alimama
from libs.mysql import ConnectMysql
from bs4 import BeautifulSoup
from libs.groupMessage import FormData
from libs.movie import SharMovie
from libs import utils
from libs.tuling import tuling
from libs.wx_bot import *
from libs.orther import Orther


logger = utils.init_logger()
al = Alimama(logger)
mjd = MediaJd()
tu = tuling()
ort = Orther()
config = configparser.ConfigParser()
config.read('config.conf',encoding="utf-8-sig")

class TextMessage(object):
    def __init__(self):
        pass

    def is_valid_date(self, str):
        try:
            time.strptime(str, "%Y-%m-%d")
            return True
        except:
            return False

    def getText(self, msg):
        wei_info = itchat.search_friends(userName=msg['FromUserName'])
        bot_info = itchat.search_friends(userName=msg['ToUserName'])

        patternURL = re.compile('^((https|http|ftp|rtsp|mms)?:\/\/)[^\s]+')

        pattern_bz = re.compile('^帮助$')
        pattern_profile = re.compile('^个人信息$')
        pattern_tixian = re.compile('^提现$')
        pattern_tuig = re.compile('^推广$')
        pattern_proxy = re.compile('^代理$')

        # 判断是否是URL链接
        if patternURL.search(msg['Text']) == None:

            pattern_s = re.compile('^搜')
            pattern_z = re.compile('^找')
            pattern_m = re.compile('^买')
            if (pattern_s.search(msg['Text']) != None) | (pattern_z.search(msg['Text']) != None) | (
                    pattern_m.search(msg['Text']) != None):

                res = ort.ishaveuserinfo(msg)

                if res['res'] == 'not_info':
                    ort.create_user_info(msg, 0, tool=False)

                jdurl = quote("http://jdyhq.ptjob.net/?r=search?kw=" + msg['Text'][1:], safe='/:?=&')

                tburl = quote('http://tbyhq.ptjob.net/index.php?r=l&kw=' + msg['Text'][1:], safe='/:?=&')
                text = '''
一一一一系统消息一一一一
亲，以为您找到所有【%s】优惠券,
快快点击领取吧！
京东：%s淘宝：%s
                ''' % (msg['Text'][1:], jdurl, tburl)
                itchat.send(text, msg['FromUserName'])

            elif pattern_bz.search(msg['Text']) != None:
                res = ort.ishaveuserinfo(msg)

                if res['res'] == 'not_info':
                    ort.create_user_info(msg, 0, tool=False)

                # 帮助操作
                text = '''
一一一一 系统信息 一一一一

回复【帮助】可查询指信息
回复【提现】申请账户余额提现
回复【推广】可申请机器人代理
回复【个人信息】可看个当前账户信息

回复【买+商品名称】
回复【找+商品名称】
回复【搜+商品名称】查看商品优惠券合集

分享【京东商品链接】或者【淘口令】
精准查询商品优惠券和返利信息！
分享【VIP视频链接】免费查看高清VIP视频！

优惠券使用教程：
'''+config.get('URL', 'course')+'''
跑堂优惠券常见问题：
'''+config.get('URL', 'faq')+'''
免费看电影方法：
'''+config.get('URL', 'movie')+'''
京东优惠券商城：
'''+config.get('URL', 'jdshop')+'''
淘宝优惠券商城：
'''+config.get('URL', 'tbshop')+'''
邀请好友得返利说明：
'''+config.get('URL', 'lnvit')+'''
                        '''
                itchat.send(text, msg['FromUserName'])
            elif pattern_tixian.search(msg['Text']) != None:
                cm = ConnectMysql()
                res = ort.ishaveuserinfo(msg)

                if res['res'] == 'not_info':
                    ort.create_user_info(msg, 0, tool=False)

                adminuser = itchat.search_friends(nickName=config.get('ADMIN', 'ADMIN_USER'))
                select_user_sql = "SELECT * FROM taojin_user_info WHERE wx_number='" + wei_info['NickName'] + "' AND wx_bot='"+ bot_info['NickName'] +"';"
                select_user_res = cm.ExecQuery(select_user_sql)

                if select_user_res and float(select_user_res[0][9]) > 0:
                    try:
                        # 修改余额
                        update_sql = "UPDATE taojin_user_info SET withdrawals_amount='0',update_time='" + str(
                            time.time()) + "' WHERE wx_number='" + wei_info['NickName'] + "' AND wx_bot='"+ bot_info['NickName'] +"';"

                        total_amount = float(select_user_res[0][6]) + float(select_user_res[0][9]);
                        update_total_sql = "UPDATE taojin_user_info SET total_rebate_amount='" + str(
                            total_amount) + "',update_time='" + str(time.time()) + "' WHERE wx_number='" + wei_info[
                                               'NickName'] + "' AND wx_bot='"+ bot_info['NickName'] +"';"

                        # 插入提现日志
                        insert_current_log_sql = "INSERT INTO taojin_current_log(wx_bot, username, amount, create_time) VALUES('" + \
                                                 bot_info['NickName'] + "', '" + wei_info['NickName'] + "', '" + str(
                            select_user_res[0][9]) + "', '" + str(time.time()) + "')"

                        to_admin_text = '''
一一一一 提现通知 一一一一

机器人：%s
提现人：%s
提现金额：%s 元
提现时间：%s
                                                ''' % (
                        bot_info['NickName'], wei_info['NickName'], select_user_res[0][9],
                        time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

                        to_user_text = '''
一一一一 提现信息 一一一一

提现成功！
提现金额将以微信红包的形式发放，请耐心等待！

分享【京东商品链接】或者【淘口令】
精准查询商品优惠券和返利信息！

优惠券使用教程：
'''+config.get('URL', 'course')+'''
免费看电影方法：
'''+config.get('URL', 'movie')+'''
邀请好友得返利：
'''+config.get('URL', 'lnvit')+'''
                                            '''
                        itchat.send(to_user_text, msg['FromUserName'])
                        itchat.send(to_admin_text, adminuser[0]['UserName'])

                        cm.ExecNonQuery(update_sql)
                        cm.ExecNonQuery(update_total_sql)
                        cm.ExecNonQuery(insert_current_log_sql)

                        return
                    except Exception as e:
                        text = '''
一一一一 系统信息 一一一一

提现失败，请稍后重试！                        
                                '''
                        print(e)
                        itchat.send(text, msg['FromUserName'])
                        return
                else:
                    text = '''
一一一一 提现信息 一一一一

提现申请失败，账户余额为0！
                                    '''
                    itchat.send(text, msg['FromUserName'])
                    return
            elif pattern_profile.search(msg['Text']) != None:
                cm = ConnectMysql()
                res = ort.ishaveuserinfo(msg)

                if res['res'] == 'not_info':
                    ort.create_user_info(msg, 0, tool=False)

                user_sql = "SELECT * FROM taojin_user_info WHERE wx_number='" + wei_info['NickName'] + "' AND wx_bot='"+ bot_info['NickName'] +"';"

                user_info = cm.ExecQuery(user_sql)

                current = "SELECT sum(amount) FROM taojin_current_log WHERE username='" + wei_info['NickName'] + "' AND wx_bot='"+ bot_info['NickName'] +"';"

                # friends_count_sql = "SELECT count(*) FROM taojin_user_info WHERE lnivter='" + str(
                #     user_info[0][5]) + "' AND wx_bot='"+ bot_info['NickName'] +"';"

                current_info = cm.ExecQuery(current)
                # friends_count = cm.ExecQuery(friends_count_sql)

                # 如果总提现金额不存在，赋值为0
                if current_info[0][0] == None:
                    current_info = 0
                else:
                    current_info = current_info[0][0]

                text = '''
一一一一 个人信息 一一一一

总返利金额: %s元
京东返利金额: %s元
淘宝返利金额: %s元
可提现余额: %s元
累计提现金额: %s元

累计订单量: %s
京东订单量: %s
淘宝订单量: %s
总好友返利: %s
总好友个数: %s

优惠券使用教程：
'''+config.get('URL', 'course')+'''
免费看电影方法：
'''+config.get('URL', 'movie')+'''
邀请好友得返利：
'''+config.get('URL', 'lnvit')+'''
                                    ''' % (
                user_info[0][6], user_info[0][7], user_info[0][8], user_info[0][9], current_info, user_info[0][11],
                user_info[0][12], user_info[0][13], user_info[0][19], user_info[0][20])
                cm.Close()
                itchat.send(text, msg['FromUserName'])
                return
            elif pattern_tuig.search(msg['Text']) != None:
                cm = ConnectMysql()
                res = ort.ishaveuserinfo(msg)

                if res['res'] == 'not_info':
                    ort.create_user_info(msg, 0, tool=False)

                user_sql = "SELECT * FROM taojin_user_info WHERE wx_number='" + wei_info['NickName'] + "' AND wx_bot='"+ bot_info['NickName'] +"';"

                cm.ExecQuery(user_sql)

                text = '''
一一一一 推广信息 一一一一

将机器人名片分享到群或者好友
好友添加机器人为好友
您和好友都将获取0.3元现金奖励
您将永久享受好友返利提成
邀请好友得返利：
'''+config.get('URL', 'lnvit')+'''
                                '''
                itchat.send(text, msg['FromUserName'])
            elif pattern_proxy.search(msg['Text']) != None:
                res = ort.ishaveuserinfo(msg)

                if res['res'] == 'not_info':
                    ort.create_user_info(msg, 0, tool=False)
                text = '''
一一一一系统消息一一一一

您好！
点击链接：'''+config.get('URL', 'proxy')+'''
添加好友备注：跑堂优惠券代理

客服人员将尽快和您取得联系，请耐心等待!
                        '''
                itchat.send(text, msg['FromUserName'])
            elif (',' in msg['Text']) and (msg['Text'].split(',')[1].isdigit()) and (
                    len(msg['Text'].split(',')[1]) == 11):

                res2 = ort.ishaveuserinfo(msg)

                if res2['res'] == 'not_info':
                    ort.create_user_info(msg, 0, tool=False)

                res = mjd.get_jd_order(msg, msg['Text'].split(',')[0], msg['Text'].split(',')[1], wei_info)

                if res['info'] == 'success':
                    itchat.send(res['user_text'], msg['FromUserName'])
                    itchat.send(res['parent_user_text'], res['parent'])
                elif res['info'] == 'order_exit':
                    itchat.send(res['send_text'], msg['FromUserName'])
                elif res['info'] == 'not_order':
                    itchat.send(res['user_text'], msg['FromUserName'])
                elif res['info'] == 'not_parent_and_success':
                    itchat.send(res['user_text'], msg['FromUserName'])
                elif res['info'] == 'not_info':
                    itchat.send('你当前没有个人账户请发送邀请人的邀请码注册个人账户！', msg['FromUserName'])
                elif res['info'] == 'feild':

                    user_text = '''
一一一一订单信息一一一一

订单返利失败！

失败原因：
【1】未确认收货（打开App确认收货后重新发送）
【2】当前商品不是通过机器人购买
【3】查询格式不正确(正确格式：2018-03-20,73462222028 )
【4】订单完成日期错误，请输入正确的订单查询日期
【6】订单号错误，请输入正确的订单号

请按照提示进行重新操作！            
                                        '''
                    itchat.send(user_text, msg['FromUserName'])
            elif ('，' in msg['Text']) and (msg['Text'].split('，')[1].isdigit()) and (
                    len(msg['Text'].split('，')[1]) == 11):
                res2 = ort.ishaveuserinfo(msg)

                if res2['res'] == 'not_info':
                    ort.create_user_info(msg, 0, tool=False)

                res = mjd.get_jd_order(msg, msg['Text'].split('，')[0], msg['Text'].split('，')[1], wei_info)

                if res['info'] == 'success':
                    itchat.send(res['user_text'], msg['FromUserName'])
                    itchat.send(res['parent_user_text'], res['parent'])
                elif res['info'] == 'order_exit':
                    itchat.send(res['send_text'], msg['FromUserName'])
                elif res['info'] == 'not_order':
                    itchat.send(res['user_text'], msg['FromUserName'])
                elif res['info'] == 'not_parent_and_success':
                    itchat.send(res['user_text'], msg['FromUserName'])
                elif res['info'] == 'not_info':
                    itchat.send('你当前没有个人账户请发送邀请人的邀请码注册个人账户！', msg['FromUserName'])
                elif res['info'] == 'feild':

                    user_text = '''
一一一一订单信息一一一一

订单返利失败！

失败原因：
【1】未确认收货（打开App确认收货后重新发送）
【2】当前商品不是通过机器人购买
【3】查询格式不正确(正确格式：2018-03-20,73462222028 )
【4】订单完成日期错误，请输入正确的订单查询日期
【6】订单号错误，请输入正确的订单号

请按照提示进行重新操作！            
                                        '''

                    itchat.send(user_text, msg['FromUserName'])
            elif (',' in msg['Text']) and (msg['Text'].split(',')[1].isdigit()) and (
                    len(msg['Text'].split(',')[1]) == 18):
                res2 = ort.ishaveuserinfo(msg)

                if res2['res'] == 'not_info':
                    ort.create_user_info(msg, 0, tool=False)

                res = al.get_order(msg, msg['Text'].split(',')[0], msg['Text'].split(',')[1], wei_info)

                if res['info'] == 'success':
                    itchat.send(res['user_text'], msg['FromUserName'])
                    itchat.send(res['parent_user_text'], res['parent'])
                    return
                elif res['info'] == 'order_exit':
                    itchat.send(res['send_text'], msg['FromUserName'])
                elif res['info'] == 'not_order':
                    itchat.send(res['user_text'], msg['FromUserName'])
                elif res['info'] == 'not_parent_and_success':
                    itchat.send(res['user_text'], msg['FromUserName'])
                elif res['info'] == 'not_info':
                    itchat.send('你当前没有个人账户请发送邀请人的邀请码注册个人账户！', msg['FromUserName'])
                elif res['info'] == 'feild':
                    user_text = '''
一一一一订单信息一一一一

订单返利失败！

失败原因：
【1】未确认收货（打开App确认收货后重新发送）
【2】当前商品不是通过机器人购买
【3】查询格式不正确(正确格式：2018-03-20,73462222028 )
【4】订单完成日期错误，请输入正确的订单查询日期
【6】订单号错误，请输入正确的订单号

请按照提示进行重新操作！            
                                        '''

                    itchat.send(user_text, msg['FromUserName'])
            elif ('，' in msg['Text']) and (msg['Text'].split('，')[1].isdigit()) and (
                    len(msg['Text'].split('，')[1]) == 18):
                res2 = ort.ishaveuserinfo(msg)

                if res2['res'] == 'not_info':
                    ort.create_user_info(msg, 0, tool=False)

                res = al.get_order(msg, msg['Text'].split('，')[0], msg['Text'].split('，')[1], wei_info)

                if res['info'] == 'success':
                    itchat.send(res['user_text'], msg['FromUserName'])
                    itchat.send(res['parent_user_text'], res['parent'])
                    return
                elif res['info'] == 'order_exit':
                    itchat.send(res['send_text'], msg['FromUserName'])
                elif res['info'] == 'not_order':
                    itchat.send(res['user_text'], msg['FromUserName'])
                elif res['info'] == 'not_parent_and_success':
                    itchat.send(res['user_text'], msg['FromUserName'])
                elif res['info'] == 'not_info':
                    itchat.send('你当前没有个人账户请发送邀请人的邀请码注册个人账户！', msg['FromUserName'])
                elif res['info'] == 'feild':
                    user_text = '''
一一一一订单信息一一一一

订单返利失败！

失败原因：
【1】未确认收货（打开App确认收货后重新发送）
【2】当前商品不是通过机器人购买
【3】查询格式不正确(正确格式：2018-03-20,73462222028 )
【4】订单完成日期错误，请输入正确的订单查询日期
【6】订单号错误，请输入正确的订单号

请按照提示进行重新操作！            
                                        '''

                    itchat.send(user_text, msg['FromUserName'])
            elif (',' in msg['Text']) and (self.is_valid_date(msg['Text'].split(',')[0])):
                user_text = '''
一一一一系统消息一一一一

查询失败！信息格式有误！
正确格式如下：
订单完成时间+逗号+订单号
(京东订单号长度11位，淘宝订单号长度18位)
例如：
2018-03-03,123456765432

请确认修改后重新发送
                                        '''
                itchat.send(user_text, msg['FromUserName'])
            elif ('，' in msg['Text']) and (self.is_valid_date(msg['Text'].split('，')[0])):
                user_text = '''
一一一一系统消息一一一一

查询失败！信息格式有误！
正确格式如下：
订单完成时间+逗号+订单号
(京东订单号长度11位，淘宝订单号长度18位)
例如：
2018-03-03,123456765432

请确认修改后重新发送
                                        '''
                itchat.send(user_text, msg['FromUserName'])
            else:
                msg_text = tu.tuling(msg)
                itchat.send(msg_text, msg['FromUserName'])
                return
        else:
            res2 = ort.ishaveuserinfo(msg)

            if res2['res'] == 'not_info':
                ort.create_user_info(msg, 0, tool=False)

            mjd.getJd(msg, msg['Text'])

    def getGroupText(self, msg):
        cm = ConnectMysql()
        wei_info = itchat.search_friends(userName=msg['FromUserName'])

        patternURL = re.compile('^((https|http|ftp|rtsp|mms)?:\/\/)[^\s]+')

        pattern_bz = re.compile('^帮助$')
        pattern_tuig = re.compile('^推广$')
        pattern_proxy = re.compile('^代理$')

        # 判断是否是URL链接
        if patternURL.search(msg['Text']) == None:

            pattern_s = re.compile('^搜')
            pattern_z = re.compile('^找')
            pattern_m = re.compile('^买')
            if (pattern_s.search(msg['Text']) != None) | (pattern_z.search(msg['Text']) != None) | (
                    pattern_m.search(msg['Text']) != None):

                jdurl = quote("http://jdyhq.ptjob.net/?r=search?kw=" + msg['Text'][1:], safe='/:?=&')

                tburl = quote('http://tbyhq.ptjob.net/index.php?r=l&kw=' + msg['Text'][1:], safe='/:?=&')
                text = '''
一一一一系统消息一一一一

亲，以为您找到所有【%s】优惠券,快快点击领取吧！

京东：%s
淘宝：%s
                        ''' % (msg['Text'][1:], jdurl, tburl)
                itchat.send(text, msg['FromUserName'])

            elif pattern_bz.search(msg['Text']) != None:
                # 帮助操作
                text = '''
一一一一 系统信息 一一一一

回复【帮助】可查询指信息
回复【提现】申请账户余额提现
回复【推广】可申请机器人代理
回复【个人信息】可看个当前账户信息

回复【买+商品名称】
回复【找+商品名称】
回复【搜+商品名称】查看商品优惠券合集

分享【京东商品链接】或者【淘口令】
精准查询商品优惠券和返利信息！
分享【VIP视频链接】免费查看高清VIP视频！

优惠券使用教程：
'''+config.get('URL', 'course')+'''
跑堂优惠券常见问题：
'''+config.get('URL', 'faq')+'''
免费看电影方法：
'''+config.get('URL', 'movie')+'''
京东优惠券商城：
'''+config.get('URL', 'jdshop')+'''
淘宝优惠券商城：
'''+config.get('URL', 'tbshop')+'''
邀请好友得返利说明：
'''+config.get('URL', 'lnvit')+'''
                        '''
                itchat.send(text, msg['FromUserName'])
            elif pattern_tuig.search(msg['Text']) != None:
                text = '''
一一一一 推广信息 一一一一

将机器人名片分享到群或者好友
好友添加机器人为好友
您和好友都将获取0.3元现金奖励
您将永久享受好友返利提成
邀请好友得返利说明：
'''+config.get('URL', 'lnvit')+'''
                                '''
                itchat.send(text, msg['FromUserName'])
            elif pattern_proxy.search(msg['Text']) != None:
                text = '''
一一一一系统消息一一一一

您好！
点击链接：'''+config.get('URL', 'proxy')+'''
添加好友备注：跑堂优惠券代理

客服人员将尽快和您取得联系，请耐心等待！
                        '''
                itchat.send(text, msg['FromUserName'])
            else:
                return
        else:
            ort.text_reply(msg, msg['Text'])