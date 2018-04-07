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


logger = utils.init_logger()

mjd = MediaJd()
mjd.login()
al = Alimama(logger)
al.login()


def getTulingText(url):
    page = requests.get(url)
    text = page.text
    return text

def tuling(msg):
    print('图灵')
    # 图灵Key
    key = '069f41c6c6924260b9d1bbdc24affd07'
    api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='

    request = api + msg['Text']
    response = getTulingText(request)
    dic_json = json.loads(response)
    return dic_json['text']

def text_reply(msg, good_url):
    cm = ConnectMysql()
    print('开始查询分享商品的信息......', msg['Text'])

    wei_info = itchat.search_friends(userName=msg['FromUserName'])

    sku_arr = good_url.split('https://item.m.jd.com/product/')

    if sku_arr == None:
        msg_text = tuling(msg)
        print(msg_text)
        itchat.send(msg_text, msg['FromUserName'])
        return

    sku = sku_arr[1].split('.')

    res = mjd.get_good_link(sku[0])
    logger.debug(res)
    if res['data']['shotCouponUrl'] == '':
        text = '''
一一一一返利信息一一一一

【商品名】%s

【京东价】%s元
【返红包】%s元
 返利链接:%s

省钱步骤：
1,点击链接，进入下单
2,订单完成后，将订单完成日期和订单号发给我哦！
例如：
2018-01-01,12345678901
        ''' % (res['logTitle'], res['logUnitPrice'], res['rebate'], res['data']['shotUrl'])
        itchat.send(text, msg['FromUserName'])

        insert_sql = "INSERT INTO taojin_query_record(good_title, good_price, good_coupon, username, create_time) VALUES('" + \
                     res['logTitle'] + "', '" + str(res['logUnitPrice']) + "', '0', '" + wei_info['NickName'] + "', '" + str(time.time()) + "')"
        cm.ExecNonQuery(insert_sql)
        return
    else:
        text = '''
一一一一返利信息一一一一

【商品名】%s

【京东价】%s元
【优惠券】%s元
【券后价】%s元
【返红包】%s元
 领券链接:%s

省钱步骤：
1,点击链接领取优惠券，正常下单购买！
2,订单完成后，将订单完成日期和订单号发给我哦！
例如：
2018-01-01,12345678901
        ''' % (res['logTitle'], res['logUnitPrice'], res['youhuiquan_price'], res['coupon_price'], res['rebate'],
               res['data']['shotCouponUrl'])

        insert_sql = "INSERT INTO taojin_query_record(good_title, good_price, good_coupon, username, create_time) VALUES('" + \
                     res['logTitle'] + "', '" + str(res['logUnitPrice']) + "', '" + res['coupon_price2'] + "', '" + wei_info['NickName'] + "', '" + str(time.time()) + "')"
        cm.ExecNonQuery(insert_sql)

        itchat.send(text, msg['FromUserName'])
        return

# 检查是否是淘宝链接
def check_if_is_tb_link(msg):
    wei_info = itchat.search_friends(userName=msg['FromUserName'])
    bot_info = itchat.search_friends(userName=msg['ToUserName'])

    cm = ConnectMysql()
    if re.search(r'【.*】', msg['Text']) and (
            u'打开👉手机淘宝👈' in msg['Text'] or u'打开👉天猫APP👈' in msg['Text'] or u'打开👉手淘👈' in msg['Text']):
        try:
            res = ishaveuserinfo(msg)

            if res['res'] == 'not_info':
                create_user_info(msg, 0, tool=False)

            q = re.search(r'【.*】', msg['Text']).group().replace(u'【', '').replace(u'】', '')
            if u'打开👉天猫APP👈' in msg['Text']:
                try:
                    url = re.search(r'http://.* \)', msg['Text']).group().replace(u' )', '')
                except:
                    url = None

            else:
                try:
                    url = re.search(r'http://.* ，', msg['Text']).group().replace(u' ，', '')
                except:
                    url = None

            if url is None:
                taokoulingurl = 'http://www.taokouling.com/index.php?m=api&a=taokoulingjm'
                taokouling = re.search(r'￥.*?￥', msg['Text']).group()
                parms = {'username': 'wx_tb_fanli', 'password': 'wx_tb_fanli', 'text': taokouling}
                res = requests.post(taokoulingurl, data=parms)
                url = res.json()['url'].replace('https://', 'http://')
                info = "tkl url: {}".format(url)

            real_url = al.get_real_url(url)
            info = "real_url: {}".format(real_url)

            res = al.get_detail(real_url, msg)
            if res == 'no match item':
                text = '''
一一一一 返利信息 一一一一

返利失败，该商品暂无优惠券信息！

分享【京东商品链接】或者【淘口令】
精准查询商品优惠券和返利信息

优惠券使用教程：
http://t.cn/RnAKqWW
常见问题解答：
http://t.cn/RnAK1w0
免费看电影方法：
http://t.cn/RnAKMul
邀请好友得返利：
http://t.cn/RnAKafe
                        '''
                itchat.send(text, msg['FromUserName'])
                return

            auctionid = res['auctionId']
            coupon_amount = res['couponAmount']
            tk_rate = res['tkRate']
            price = res['zkPrice']
            fx2 = round(float(res['tkCommonFee']) * 0.3, 2)
            real_price = round(price - coupon_amount, 2)
            res1 = al.get_tk_link(auctionid)

            if res1 == None:
                img = al.get_qr_image()
                itchat.send(img, msg['FromUserName'])
                return
            tao_token = res1['taoToken']
            short_link = res1['shortLinkUrl']
            coupon_link = res1['couponLink']
            if coupon_link != "":
                coupon_token = res1['couponLinkTaoToken']
                res_text = '''
一一一一返利信息一一一一

【商品名】%s元

【淘宝价】%s元
【优惠券】%s元
【券后价】%s元
【返红包】%.2f元
【淘口令】%s

省钱步骤：
1,复制本条信息打开淘宝App领取优惠券下单！
2,订单完成后，将订单完成日期和订单号发给我哦！
例如：
2018-01-01,12345678901
                ''' % (q, price, coupon_amount, real_price, fx2, coupon_token)
            else:
                res_text = '''
一一一一返利信息一一一一

【商品名】%s
【淘宝价】%s元
【返红包】%.2f元
【淘口令】%s

省钱步骤：
1,复制本条信息打开淘宝App领取优惠券下单！
2,订单完成后，将订单完成日期和订单号发给我哦！
例如：
2018-01-01,12345678901
                                ''' % (q, price, fx2, tao_token)

            itchat.send(res_text, msg['FromUserName'])
        except Exception as e:
            trace = traceback.format_exc()
            logger.warning("error:{},trace:{}".format(str(e), trace))
            info = '''
一一一一 返利信息 一一一一

返利失败，该商品暂无优惠券信息！

分享【京东商品链接】或者【淘口令】
精准查询商品优惠券和返利信息

优惠券使用教程：
http://t.cn/RnAKqWW
常见问题解答：
http://t.cn/RnAK1w0
免费看电影方法：
http://t.cn/RnAKMul
邀请好友得返利：
http://t.cn/RnAKafe
            '''
            return info

    elif msg['Type'] == 'Sharing':
        res = ishaveuserinfo(msg)

        if res['res'] == 'not_info':
            create_user_info(msg, 0, tool=False)
        htm = re.findall(r"<appname>.*?</appname>", msg['Content'])

        if (htm):
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
                    itchat.send(text, msg['FromUserName'])
                    return

        text_reply(msg, msg['Url'])
    # elif msg['Text'].isdigit() and len(msg['Text']) == 6:
    #     lnivt_user(msg)
    # elif msg['Text'] == '10000':
    #     tool = False
    #     create_user_info(msg, 0, tool)
    elif msg['Type'] == 'Text':

        patternURL = re.compile('^((https|http|ftp|rtsp|mms)?:\/\/)[^\s]+')

        pattern_bz = re.compile('^帮助$')
        pattern_profile = re.compile('^个人信息$')
        pattern_tixian = re.compile('^提现$')
        pattern_tuig = re.compile('^推广$')
        pattern_proxy = re.compile('^代理$')
        pattern_movie = re.compile('^找电影')

        # 判断是否是URL链接
        if patternURL.search(msg['Text']) == None:

            pattern_s = re.compile('^搜')
            pattern_z = re.compile('^找')
            pattern_m = re.compile('^买')
            if (pattern_s.search(msg['Text']) != None) | (pattern_z.search(msg['Text']) != None) | (
                    pattern_m.search(msg['Text']) != None):

                res = ishaveuserinfo(msg)

                if res['res'] == 'not_info':
                    create_user_info(msg, 0, tool=False)

                jdurl = quote("http://jdyhq.ptjob.net/?r=search?kw=" + msg['Text'][1:], safe='/:?=&')

                tbyhq = requests.get('http://tbyhq.ptjob.net')

                # 使用BeautifulSoup解析HTML，并提取淘宝优惠券页面token
                soup = BeautifulSoup(tbyhq.text, 'lxml')

                token = soup.find(attrs={'name': 'token'})

                tburl = quote('http://tbyhq.ptjob.net/?r=find?kw=' + msg['Text'][1:] + '&token=' + token.get('value'),
                              safe='/:?=&')
                text = '''
一一一一系统消息一一一一

亲，以为您找到所有【%s】优惠券,快快点击领取吧！

京东：%s
淘宝：%s
                        ''' % (msg['Text'][1:], jdurl, tburl)
                itchat.send(text, msg['FromUserName'])

            elif pattern_bz.search(msg['Text']) != None:
                res = ishaveuserinfo(msg)

                if res['res'] == 'not_info':
                    create_user_info(msg, 0, tool=False)

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
http://t.cn/RnAKqWW
跑堂优惠券常见问题：
http://t.cn/RnAK1w0
免费看电影方法：
http://t.cn/RnAKMul
京东优惠券商城：
http://jdyhq.ptjob.net
淘宝优惠券商城：
http://tbyhq.ptjob.net
邀请好友得返利说明：
http://t.cn/RnAKafe
                '''
                itchat.send(text, msg['FromUserName'])
            elif pattern_tixian.search(msg['Text']) != None:
                res = ishaveuserinfo(msg)

                if res['res'] == 'not_info':
                    create_user_info(msg, 0, tool=False)

                select_user_sql = "SELECT * FROM taojin_user_info WHERE wx_number='" + wei_info['NickName'] + "';"
                select_user_res = cm.ExecQuery(select_user_sql)

                if select_user_res and float(select_user_res[0][8]) > 0:
                    try:
                        # 修改余额
                        update_sql = "UPDATE taojin_user_info SET withdrawals_amount='0',update_time='" + str(
                            time.time()) + "' WHERE wx_number='" + wei_info['NickName'] + "';"

                        total_amount = float(select_user_res[0][5]) + float(select_user_res[0][8]);
                        update_total_sql = "UPDATE taojin_user_info SET total_rebate_amount='" + str(
                            total_amount) + "',update_time='" + str(time.time()) + "' WHERE wx_number='" + wei_info['NickName'] + "';"

                        # 插入提现日志
                        insert_current_log_sql = "INSERT INTO taojin_current_log(wx_bot, username, amount, create_time) VALUES('" + \
                                                 bot_info['NickName'] + "', '" + wei_info['NickName'] + "', '" + str(
                            select_user_res[0][8]) + "', '" + str(time.time()) + "')"

                        to_admin_text = '''
一一一一 提现通知 一一一一

机器人：%s
提现人：%s
提现金额：%s 元
提现时间：%s
                                        ''' % (bot_info['NickName'], wei_info['NickName'], select_user_res[0][8],
                                               time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

                        to_user_text = '''
一一一一 提现信息 一一一一

提现成功！
提现金额将以微信红包的形式发放，请耐心等待！

分享【京东商品链接】或者【淘口令】
精准查询商品优惠券和返利信息！

优惠券使用教程：
http://t.cn/RnAKqWW
免费看电影方法：
http://t.cn/RnAKMul
邀请好友得返利：
http://t.cn/RnAKafe
                                    '''
                        itchat.send(to_user_text, msg['FromUserName'])
                        itchat.send(to_admin_text, '@2270c9a6e8ce6bef9305c511a1ff49ea478544d6fe9430085f50c24fbe4ae6f1')

                        update_res = cm.ExecNonQuery(update_sql)
                        update_res = cm.ExecNonQuery(update_total_sql)
                        insert_current_log_res = cm.ExecNonQuery(insert_current_log_sql)

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

提现申请失败，请稍后重试！
                            '''
                    itchat.send(text, msg['FromUserName'])
                    return
            elif pattern_profile.search(msg['Text']) != None:
                res = ishaveuserinfo(msg)

                if res['res'] == 'not_info':
                    create_user_info(msg, 0, tool=False)

                user_sql = "SELECT * FROM taojin_user_info WHERE wx_number='" + wei_info['NickName'] + "';"

                user_info = cm.ExecQuery(user_sql)

                if len(user_info) < 1:
                    send_text = '''
一一一一 个人信息 一一一一

你还没创建个人账户哦！

回复【邀请码】创建个人账户哦!
还可以领取现金红包哦！

优惠券使用教程：
http://t.cn/RnAKqWW
免费看电影方法：
http://t.cn/RnAKMul
邀请好友得返利：
http://t.cn/RnAKafe
                    '''
                    cm.Close()
                    itchat.send(send_text, msg['FromUserName'])
                    return

                current = "SELECT sum(amount) FROM taojin_current_log WHERE username='" + wei_info['NickName'] + "';"

                friends_count_sql = "SELECT count(*) FROM taojin_user_info WHERE lnivter='" + str(
                    user_info[0][4]) + "';"

                current_info = cm.ExecQuery(current)
                print(current_info)
                friends_count = cm.ExecQuery(friends_count_sql)

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
http://t.cn/RnAKqWW
免费看电影方法：
http://t.cn/RnAKMul
邀请好友得返利：
http://t.cn/RnAKafe
                                ''' % (
                    user_info[0][5], user_info[0][6], user_info[0][7], user_info[0][8], current_info, user_info[0][10],
                    user_info[0][11], user_info[0][12], user_info[0][18], friends_count[0][0], user_info[0][4])
                cm.Close()
                itchat.send(text, msg['FromUserName'])
                return
            elif pattern_tuig.search(msg['Text']) != None:
                res = ishaveuserinfo(msg)

                if res['res'] == 'not_info':
                    create_user_info(msg, 0, tool=False)

                user_sql = "SELECT * FROM taojin_user_info WHERE wx_number='" + wei_info['NickName'] + "';"

                user_info = cm.ExecQuery(user_sql)

                text = '''
一一一一 推广信息 一一一一

将机器人名片分享到群或者好友
好友添加机器人为好友
您和好友都将获取0.3元现金奖励
您将永久享受好友返利提成
邀请好友返利说明：
http://t.cn/RnAKafe
                        ''' % (user_info[0][4])
                itchat.send(text, msg['FromUserName'])
            elif pattern_proxy.search(msg['Text']) != None:
                res = ishaveuserinfo(msg)

                if res['res'] == 'not_info':
                    create_user_info(msg, 0, tool=False)

                to_admin_text = '''
一一一一 申请代理通知 一一一一

机器人：%s
申请人：%s
申请代理时间：%s
                            ''' % (
                bot_info['NickName'], wei_info['NickName'], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                text = '''
一一一一系统消息一一一一

您好！
点击链接：http://t.cn/Rf0LUP0
添加好友备注：跑堂优惠券代理

客服人员将尽快和您取得联系，请耐心等待！
                        '''
                itchat.send(text, msg['FromUserName'])
                itchat.send(to_admin_text, '@2270c9a6e8ce6bef9305c511a1ff49ea478544d6fe9430085f50c24fbe4ae6f1')
            elif (',' in msg['Text']) and (msg['Text'].split(',')[1].isdigit()) and (len(msg['Text'].split(',')[1]) == 11):

                res2 = ishaveuserinfo(msg)

                if res2['res'] == 'not_info':
                    create_user_info(msg, 0, tool=False)

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
            elif ('，' in msg['Text']) and (msg['Text'].split('，')[1].isdigit()) and (len(msg['Text'].split('，')[1]) == 11):
                res2 = ishaveuserinfo(msg)

                if res2['res'] == 'not_info':
                    create_user_info(msg, 0, tool=False)

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
            elif (',' in msg['Text']) and (msg['Text'].split(',')[1].isdigit()) and (len(msg['Text'].split(',')[1]) == 18):
                res2 = ishaveuserinfo(msg)

                if res2['res'] == 'not_info':
                    create_user_info(msg, 0, tool=False)

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
            elif ('，' in msg['Text']) and (msg['Text'].split('，')[1].isdigit()) and (len(msg['Text'].split('，')[1]) == 18):
                res2 = ishaveuserinfo(msg)

                if res2['res'] == 'not_info':
                    create_user_info(msg, 0, tool=False)

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
            elif (',' in msg['Text']) and (is_valid_date(msg['Text'].split(',')[0])):
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
            elif ('，' in msg['Text']) and (is_valid_date(msg['Text'].split('，')[0])):
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
                msg_text = tuling(msg)
                itchat.send(msg_text, msg['FromUserName'])
                return
        else:
            res2 = ishaveuserinfo(msg)

            if res2['res'] == 'not_info':
                create_user_info(msg, 0, tool=False)

            text_reply(msg, msg['Text'])

# 检查是否是淘宝链接
def check_if_is_group(msg):
    cm = ConnectMysql()
    if re.search(r'【.*】', msg['Text']) and (
            u'打开👉手机淘宝👈' in msg['Text'] or u'打开👉天猫APP👈' in msg['Text'] or u'打开👉手淘👈' in msg['Text']):
        try:
            q = re.search(r'【.*】', msg['Text']).group().replace(u'【', '').replace(u'】', '')
            if u'打开👉天猫APP👈' in msg['Text']:
                try:
                    url = re.search(r'http://.* \)', msg['Text']).group().replace(u' )', '')
                except:
                    url = None

            else:
                try:
                    url = re.search(r'http://.* ，', msg['Text']).group().replace(u' ，', '')
                except:
                    url = None

            if url is None:
                taokoulingurl = 'http://www.taokouling.com/index.php?m=api&a=taokoulingjm'
                taokouling = re.search(r'￥.*?￥', msg['Text']).group()
                parms = {'username': 'wx_tb_fanli', 'password': 'wx_tb_fanli', 'text': taokouling}
                res = requests.post(taokoulingurl, data=parms)
                url = res.json()['url'].replace('https://', 'http://')
                info = "tkl url: {}".format(url)

            real_url = al.get_real_url(url)
            info = "real_url: {}".format(real_url)

            res = al.get_group_detail(real_url, msg)
            print(res)
            if res == 'no match item':
                text = '''
        一一一一 返利信息 一一一一

        返利失败，该商品暂无优惠券信息！

        分享【京东商品链接】或者【淘口令】
        精准查询商品优惠券和返利信息

        优惠券使用教程：
        http://t.cn/RnAKqWW
        常见问题解答：
        http://t.cn/RnAK1w0
        免费看电影方法：
        http://t.cn/RnAKMul
        邀请好友得返利：
        http://t.cn/RnAKafe
                        '''
                itchat.send(text, msg['FromUserName'])
                return

            auctionid = res['auctionId']
            coupon_amount = res['couponAmount']
            tk_rate = res['tkRate']
            price = res['zkPrice']
            fx2 = round(float(res['tkCommonFee']) * 0.3, 2)
            real_price = round(price - coupon_amount, 2)
            res1 = al.get_tk_link(auctionid)

            if res1 == None:
                img = al.get_qr_image()
                itchat.send(img, msg['FromUserName'])
                return
            tao_token = res1['taoToken']
            short_link = res1['shortLinkUrl']
            coupon_link = res1['couponLink']
            if coupon_link != "":
                coupon_token = res1['couponLinkTaoToken']
                res_text = '''
        一一一一返利信息一一一一

        【商品名】%s元

        【淘宝价】%s元
        【优惠券】%s元
        【券后价】%s元
        【返红包】%.2f元
        【淘口令】%s

        省钱步骤：
        1,复制本条信息打开淘宝App领取优惠券下单！
        2,订单完成后，将订单完成日期和订单号发给我哦！
        例如：
        2018-01-01,12345678901
                ''' % (q, price, coupon_amount, real_price, fx2, coupon_token)
            else:
                res_text = '''
        一一一一返利信息一一一一

        【商品名】%s
        【淘宝价】%s元
        【返红包】%.2f元
        【淘口令】%s

        省钱步骤：
        1,复制本条信息打开淘宝App领取优惠券下单！
        2,订单完成后，将订单完成日期和订单号发给我哦！
        例如：
        2018-01-01,12345678901
                                ''' % (q, price, fx2, tao_token)

            itchat.send(res_text, msg['FromUserName'])
        except Exception as e:
            trace = traceback.format_exc()
            logger.warning("error:{},trace:{}".format(str(e), trace))
            info = '''
一一一一 返利信息 一一一一

返利失败，该商品暂无优惠券信息！

分享【京东商品链接】或者【淘口令】
精准查询商品优惠券和返利信息

优惠券使用教程：
http://t.cn/RnAKqWW
常见问题解答：
http://t.cn/RnAK1w0
免费看电影方法：
http://t.cn/RnAKMul
邀请好友得返利：
http://t.cn/RnAKafe
            '''
            itchat.send(info, msg['FromUserName'])
            return

    elif msg['Type'] == 'Sharing':

        htm = re.findall(r"<appname>.*?</appname>", msg['Content'])

        if (htm):
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
邀请好友得返利：
http://t.cn/RnAKafe
                    ''' % (player_url)
                    itchat.send(text, msg['FromUserName'])
                    return

        text_reply(msg, msg['Url'])
    elif msg['Type'] == 'Text':

        patternURL = re.compile('^((https|http|ftp|rtsp|mms)?:\/\/)[^\s]+')

        pattern_bz = re.compile('^帮助$')
        pattern_profile = re.compile('^个人信息$')
        pattern_tixian = re.compile('^提现$')
        pattern_tuig = re.compile('^推广$')
        pattern_proxy = re.compile('^代理$')
        pattern_movie = re.compile('^找电影')

        # 判断是否是URL链接
        if patternURL.search(msg['Text']) == None:

            pattern_s = re.compile('^搜')
            pattern_z = re.compile('^找')
            pattern_m = re.compile('^买')
            if (pattern_s.search(msg['Text']) != None) | (pattern_z.search(msg['Text']) != None) | (
                    pattern_m.search(msg['Text']) != None):

                jdurl = quote("http://jdyhq.ptjob.net/?r=search?kw=" + msg['Text'][1:], safe='/:?=&')

                tbyhq = requests.get('http://tbyhq.ptjob.net')

                # 使用BeautifulSoup解析HTML，并提取淘宝优惠券页面token
                soup = BeautifulSoup(tbyhq.text, 'lxml')

                token = soup.find(attrs={'name': 'token'})

                tburl = quote('http://tbyhq.ptjob.net/?r=find?kw=' + msg['Text'][1:] + '&token=' + token.get('value'),
                              safe='/:?=&')
                text = '''
一一一一优惠券集合一一一一

亲，已为您找到所有【%s】优惠券,快快点击领取吧！

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

分享【京东商品链接】或者【淘口令】精准查询商品优惠券和返利信息！
分享【VIP视频链接】免费查看高清VIP视频！

优惠券使用教程：
http://t.cn/RnAKqWW
跑堂优惠券常见问题：
http://t.cn/RnAK1w0
免费看电影方法：
http://t.cn/RnAKMul
京东优惠券商城：
http://jdyhq.ptjob.net
淘宝优惠券商城：
http://tbyhq.ptjob.net
邀请好友得返利说明：
http://t.cn/RnAKafe
                '''
                itchat.send(text, msg['FromUserName'])
            elif pattern_proxy.search(msg['Text']) != None:

                bot_res = itchat.search_friends(userName=msg['ToUserName'])
                user_res = itchat.search_friends(userName=msg['FromUserName'])

                to_admin_text = '''
一一一一 申请代理通知 一一一一

机器人：%s
申请人：%s
申请代理时间：%s
                            ''' % (
                bot_res['NickName'], user_res['NickName'], time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
                text = '''
一一一一系统消息一一一一

您好！
点击链接：http://t.cn/Rf0LUP0
添加好友备注：跑堂优惠券代理

客服人员将尽快和您取得联系，请耐心等待！
                        '''
                itchat.send(text, msg['FromUserName'])
                itchat.send(to_admin_text, '@2270c9a6e8ce6bef9305c511a1ff49ea478544d6fe9430085f50c24fbe4ae6f1')
        else:
            text_reply(msg, msg['Text'])

def is_valid_date(str):
    '''判断是否是一个有效的日期字符串'''
    try:
        time.strptime(str, "%Y-%m-%d")
        return True
    except:
        return False

# 创建用户账户
def create_user_info(msg, lnivt_code=0, tool=False):
    cm = ConnectMysql()

    if tool==False:
        res = itchat.search_friends(userName=msg['FromUserName'])
    else:
        res = itchat.search_friends(userName=msg['RecommendInfo']['UserName'])

    while True:
        # 生成随机数
        randNum = random.randint(100000, 999999)

        # 定义SQL语句 查询数据是否已经存在
        select_sql = "SELECT * FROM taojin_user_info WHERE lnivt_code=" + str(randNum) + ""

        select_res = cm.ExecQuery(select_sql)

        if len(select_res) == 0:
            break

    if lnivt_code == 0:
        sql = "INSERT INTO taojin_user_info(wx_number, sex, nickname, lnivt_code, withdrawals_amount, lnivter, create_time) VALUES('" + \
              res['NickName'] + "', '" + str(res['Sex']) + "', '" + res['NickName'] + "', '" + str(
            randNum) + "', '0.3', '" + str(lnivt_code) + "', '" + str(round(time.time())) + "');"

        insert_res = cm.ExecNonQuery(sql)
        # 日志参数
        args = {
            'username': res['NickName'],
            'rebate_amount': 0.3,
            'type': 1,
            'create_time': time.time()
        }
        # 写入返利日志
        cm.InsertRebateLog(args)
        return
    else:
        lnivt_2_info = itchat.search_friends(nickName=lnivt_code)

        lnivter_sql = "SELECT * FROM taojin_user_info WHERE nickname='" + lnivt_code + "' LIMIT 1;"
        # 获取邀请人信息
        lnivt_info = cm.ExecQuery(lnivter_sql)
        # 有邀请人时，插入用户信息，并奖励邀请人
        sql = "INSERT INTO taojin_user_info(wx_number, sex, nickname, lnivt_code, withdrawals_amount, lnivter, create_time) VALUES('" + \
              res['NickName'] + "', '" + str(res['Sex']) + "', '" + res['NickName'] + "', '" + str(
            randNum) + "', '0.3', '" + str(lnivt_code) + "', '" + str(round(time.time())) + "');"

        # 给邀请人余额加0.3元奖励
        jianli = round(float(lnivt_info[0][8]) + 0.3, 2)

        friends_num = int(lnivt_info[0][19]) + 1

        cm.ExecNonQuery("UPDATE taojin_user_info SET withdrawals_amount='" + str(
            jianli) + "', friends_number='" + str(friends_num) + "'  WHERE nickname='" + lnivt_code + "';")

        cm.ExecNonQuery(sql)

        # 日志参数
        args = {
            'username': res['NickName'],
            'rebate_amount': 0.3,
            'type': 1,
            'create_time': time.time()
        }

        args2 = {
            'username': lnivt_info[0][1],
            'rebate_amount': 0.3,
            'type': 2,
            'create_time': time.time()
        }

        # 写入返利日志
        cm.InsertRebateLog(args)
        cm.InsertRebateLog(args2)
        user_sql = "SELECT * FROM taojin_user_info WHERE wx_number='" + res['NickName'] + "';"
        user_info = cm.ExecQuery(user_sql)
        lnivt_text = '''
一一一一系统消息一一一一

您的好友【%s】已邀请成功！

0.3元奖励金已到账
您将永久获得该好友永久购物返利佣金提成

邀请好友得返利说明：
http://t.cn/RnAKafe
        ''' % (user_info[0][3])

        cm.Close()
        itchat.send(lnivt_text, lnivt_2_info['UserName'])

# 使用邀请码创建账户, 或绑定邀请人
def lnivt_user(msg):
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
http://t.cn/RnAKqWW
免费看电影方法：
http://t.cn/RnAKMul
邀请好友得返利：
http://t.cn/RnAKafe
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
http://t.cn/RnAKqWW
免费看电影方法：
http://t.cn/RnAKMul
邀请好友得返利：
http://t.cn/RnAKafe
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
        add_lnivt_sql = "UPDATE taojin_user_info SET lnivter='" + str(msg['Text']) + "' WHERE wx_number='" + res['NickName'] + "';"

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
http://t.cn/RnAKqWW
免费看电影方法：
http://t.cn/RnAKMul
邀请好友得返利：
http://t.cn/RnAKafe
                    ''' % (check_user_res[0][4])

            lnivt_text = '''
一一一一系统消息一一一一

您的好友【%s】已邀请成功！

0.3元奖励金已到账
您将永久获得该好友永久购物返利佣金提成

邀请好友得返利说明：
http://t.cn/RnAKafe
            ''' % (check_user_res[0][3])
            itchat.send(text, msg['FromUserName'])
            itchat.send(lnivt_text, lnivt_info[0][1])
        else:
            cm.Close()
            itchat.send('添加邀请人失败！请重试！', msg['FromUserName'])

# 判断用户是否有个人账户
def ishaveuserinfo(msg):
    cm = ConnectMysql()

    res = itchat.search_friends(userName=msg['FromUserName'])
    check_user_sql = "SELECT * FROM taojin_user_info WHERE wx_number='" + str(res['NickName']) + "';"
    check_user_res = cm.ExecQuery(check_user_sql)
    # 判断是否已经有个人账户，没有去创建
    if len(check_user_res) < 1:
        cm.Close()
        send_text = '''
一一一一 个人信息 一一一一

你还没创建个人账户哦！

回复【邀请码】创建个人账户哦!
还可以领取现金红包哦！

优惠券使用说明：
http://t.cn/RnAKqWW
                    '''
        return {"res": "not_info", "text": send_text}

    return {"res": "have_info"}

def async(f):
    def wrapper(*args, **kwargs):
        thr = Thread(target = f, args = args, kwargs = kwargs)
        thr.start()
    return wrapper

# 获取群
@async
def groupMessages():
    time.sleep(20)
    yorn = input("是否重新选群？y/n:")
    if yorn == 'n':
        start_send_msg_thread()
        return

    print('start.....')
    cm = ConnectMysql()

    res = itchat.web_init()

    select_sql = "DELETE FROM taojin_group_message WHERE username='"+str(res['User']['NickName'])+"';"
    cm.ExecNonQuery(select_sql)

    group = itchat.get_chatrooms(update=True, contactOnly=False)

    template_demo = """
    <!DOCTPE html>
    <html>
        <head>
            <meta charset="utf-8"/>
            <title>选择群聊</title>
        </head>
        <body>
            <div>
                <form action='/formdata'  method='post'>
                    <input type="hidden" name="username" value="{{ res['User']['NickName'] }}" />
                    % for item in items:
                    <input type="checkbox" name="{{ item['UserName'] }}" value="{{ item['NickName'] }}" />{{ item['NickName'] }}
                    %end
                    <input type='submit' value='提交' />
                </form>
            </div>
        </body>
    </html>
    """

    html = template(template_demo, items=group, res=res)

    with open('form.html', 'w', encoding='utf-8') as f:
        f.write(html)

    fd = FormData()
    fd.run()

# 群发消息
def send_group_meg():
    cm = ConnectMysql()

    res = itchat.web_init()

    select_sql = "SELECT * FROM taojin_group_message WHERE username='"+str(res['User']['NickName'])+"';"

    group_info = cm.ExecQuery(select_sql)

    while True:

        time.sleep(60)

        data_sql = "SELECT * FROM taojin_good_info WHERE status=1 LIMIT 1"

        data1 = cm.ExecQuery(data_sql)
        if data1 == ():
            mjd.get_good_info()
            cm.Close()
        cm2 = ConnectMysql()
        data = cm2.ExecQuery(data_sql)
        if data[0][9].isdigit() and (int(data[0][9]) == 0):
            text = '''
一一一一返利信息一一一一

【商品名】%s
【京东价】%s元
购买链接:%s

请点击链接，下单购买！
            ''' % (data[0][2], data[0][4], data[0][8])
        else:
            text = '''
一一一一返利信息一一一一

【商品名】%s
【京东价】%s元
【优惠券】%s元
【券后价】%s元
领券链接:%s

请点击链接领取优惠券，下单购买！
            ''' % (data[0][2], data[0][4], data[0][6], data[0][7], data[0][9])

        delete_sql = "UPDATE taojin_good_info SET status='2' WHERE id='"+str(data[0][0])+"'"
        cm.ExecNonQuery(delete_sql)

        img_name = data[0][3].split('/')

        img_path = "images/" + img_name[-1]
        for item in group_info:
            itchat.send_image(img_path, item[2])
            itchat.send(text, item[2])


# 启动一个线程，定时发送商品信息
def start_send_msg_thread():
    t = Thread(target=send_group_meg, args=())
    t.setDaemon(True)
    t.start()


class WxBot(object):
    def __init__(self):
        # groupMessages()
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
        itchat.add_friend(**msg['Text'])  # 该操作会自动将新好友的消息录入，不需要重载通讯录

        soup = BeautifulSoup(msg['Content'], 'lxml')

        msg_soup = soup.find('msg')

        sourc = msg_soup.get('sourcenickname')
        print(sourc)
        if sourc == '':
            sourc = 0

        create_user_info(msg, lnivt_code=sourc, tool=True)


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
            itchat.auto_login(enableCmdQR=2, hotReload=True)
        else:
            itchat.auto_login(True)
        itchat.run()
        
if __name__ == '__main__':
    mi = WxBot()
