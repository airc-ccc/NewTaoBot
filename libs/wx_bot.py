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
from libs import utils
from urllib.parse import quote
from itchat.content import *
from libs.mediaJd import MediaJd
from libs.alimama import Alimama
from libs.mysql import ConnectMysql
from bs4 import BeautifulSoup

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
    print('圖靈')
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
        ''' % (res['logTitle'], res['logUnitPrice'], res['rebate'], res['data']['shotUrl'])
        itchat.send(text, msg['FromUserName'])

        insert_sql = "INSERT INTO taojin_query_record(good_title, good_price, good_coupon, username, create_time) VALUES('" + \
                     res['logTitle'] + "', '" + str(res['logUnitPrice']) + "', '0', '" + msg[
                         'FromUserName'] + "', '" + str(time.time()) + "')"
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
        ''' % (res['logTitle'], res['logUnitPrice'], res['youhuiquan_price'], res['coupon_price'], res['rebate'],
               res['data']['shotCouponUrl'])

        insert_sql = "INSERT INTO taojin_query_record(good_title, good_price, good_coupon, username, create_time) VALUES('" + \
                     res['logTitle'] + "', '" + str(res['logUnitPrice']) + "', '" + res['coupon_price2'] + "', '" + msg[
                         'FromUserName'] + "', '" + str(time.time()) + "')"
        cm.ExecNonQuery(insert_sql)

        itchat.send(text, msg['FromUserName'])
        return


# 检查是否是淘宝链接
def check_if_is_tb_link(msg):
    cm = ConnectMysql()

    if re.search(r'【.*】', msg['Text']) and (
            u'打开👉手机淘宝👈' in msg['Text'] or u'打开👉天猫APP👈' in msg['Text'] or u'打开👉手淘👈' in msg['Text']):
        try:
            res = ishaveuserinfo(msg)

            if res['res'] == 'not_info':
                itchat.send(res['text'], msg['FromUserName'])
                return

            # print('line_38', msg['Text'])
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
                # logger.debug(info)

            # get real url
            real_url = al.get_real_url(url)
            info = "real_url: {}".format(real_url)
            # logger.debug(info)

            # get detail
            res = al.get_detail(real_url, msg)
            if res == 'no match item':
                text = '''
一一一一 系统消息 一一一一
该宝贝暂时没有找到内部返利通道！
亲您可以换个宝贝试试，也可以联系
我们群内管理员帮着寻找有返现
的类似商品             '''
                itchat.send(text, msg['FromUserName'])
                return

            # logger.debug(res)
            auctionid = res['auctionId']
            coupon_amount = res['couponAmount']
            tk_rate = res['tkRate']
            price = res['zkPrice']
            fx2 = round(float(res['tkCommonFee']) * 0.3, 2)
            real_price = price - coupon_amount
            # # get tk link
            res1 = al.get_tk_link(auctionid)

            # 判斷數據是否為樓
            if res1 == None:
                img = al.get_qr_image()
                itchat.send(img, msg['FromUserName'])
                return

            # logger.debug(res1)
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

请复制本条信息，打开淘宝APP领取优惠券！

                ''' % (q, price, coupon_amount, real_price, fx2, coupon_token)
            else:
                res_text = '''
一一一一返利信息一一一一

【商品名】%s

【返红包】%.2f元
【淘口令】%s

请复制本条信息，打开淘宝APP领取优惠券！
                                ''' % (q, fx2, tao_token)

            itchat.send(res_text, msg['FromUserName'])
        except Exception as e:
            trace = traceback.format_exc()
            logger.warning("error:{},trace:{}".format(str(e), trace))
            info = '''%s
一一一一 系统消息 一一一一
该宝贝暂时没有找到内部返利通道！
亲您可以换个宝贝试试，也可以联
系我们群内管理员帮着寻找有返现的类似商品
            ''' % q
            return info

    elif msg['Type'] == 'Sharing':
        res = ishaveuserinfo(msg)

        if res['res'] == 'not_info':
            itchat.send(res['text'], msg['FromUserName'])
            return


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
一一一一 影视信息 一一一一

查询成功！你要的影片点击下方链接即可观看！
感谢你的使用！ 链接加载速度如果较慢！
可选择浏览器中打开链接！
%s
                    ''' % (player_url)
                    itchat.send(text, msg['FromUserName'])
                    return

        text_reply(msg, msg['Url'])
    elif msg['Text'].isdigit() and len(msg['Text']) == 6:
        lnivt_user(msg)
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
                    itchat.send(res['text'], msg['FromUserName'])
                    return

                jdurl = quote("http://jdyhq.ptjob.net/?r=search?kw=" + msg['Text'][1:], safe='/:?=&')

                tbyhq = requests.get('http://tbyhq.ptjob.net')

                # 使用BeautifulSoup解析HTML，并提取淘宝优惠券页面token
                soup = BeautifulSoup(tbyhq.text, 'lxml')

                token = soup.find(attrs={'name': 'token'})

                tburl = quote('http://tbyhq.ptjob.net/?r=find?kw=' + msg['Text'][1:] + '&token=' + token.get('value'),
                              safe='/:?=&')
                text = '''
一一一一优惠券集合一一一一

【京东 淘宝 领券直降】

亲，以为您找到所有【%s】优惠券,快快点击领取吧！

京东优惠券集合：%s
淘宝优惠券集合：%s
                        ''' % (msg['Text'][1:], jdurl, tburl)
                itchat.send(text, msg['FromUserName'])

            elif pattern_bz.search(msg['Text']) != None:
                res = ishaveuserinfo(msg)

                if res['res'] == 'not_info':
                    itchat.send(res['text'], msg['FromUserName'])
                    return

                # 帮助操作
                text = '''
一一一一 系统信息 一一一一

输入【个人信息】可查询账户及余额信息
输入【帮助】可查询指信息
输入【提现】可申请账户余额提现
输入【推广】可查看邀请好友返利教程
输入【代理】可申请机器人代理

淘京机器人使用说明：
http://t.cn/RWnguQB
淘京机器人常见问题：
http://t.cn/RWn8OAc
免费看电影方法：
http://t.cn/RWnex0F
京东优惠券网站：
http://jdyhq.ptjob.net
淘宝优惠券网站：
http://tbyhq.ptjob.net
                '''
                itchat.send(text, msg['FromUserName'])
            elif pattern_tixian.search(msg['Text']) != None:
                res = ishaveuserinfo(msg)

                if res['res'] == 'not_info':
                    itchat.send(res['text'], msg['FromUserName'])
                    return

                select_user_sql = "SELECT * FROM taojin_user_info WHERE wx_number='" + msg['FromUserName'] + "';"
                select_user_res = cm.ExecQuery(select_user_sql)

                if select_user_res and float(select_user_res[0][8]) >= 1:
                    try:
                        # 修改余额
                        update_sql = "UPDATE taojin_user_info SET withdrawals_amount='0',update_time='" + str(
                            time.time()) + "' WHERE wx_number='" + msg['FromUserName'] + "';"

                        total_amount = float(select_user_res[0][5]) + float(select_user_res[0][8]);
                        update_total_sql = "UPDATE taojin_user_info SET total_rebate_amount='" + str(
                            total_amount) + "',update_time='" + str(time.time()) + "' WHERE wx_number='" + msg[
                                               'FromUserName'] + "';"

                        # 插入提现日志
                        insert_current_log_sql = "INSERT INTO taojin_current_log(wx_bot, username, amount, create_time) VALUES('" + \
                                                 msg['ToUserName'] + "', '" + msg['FromUserName'] + "', '" + str(
                            select_user_res[0][8]) + "', '" + str(time.time()) + "')"

                        bot_res = itchat.search_friends(userName=msg['ToUserName'])
                        user_res = itchat.search_friends(userName=msg['FromUserName'])
                        to_admin_text = '''
一一一一 提现通知 一一一一

机器人：%s
提现人：%s
提现金额：%s 元
提现时间：%s
                                        ''' % (bot_res['NickName'], user_res['NickName'], select_user_res[0][8],
                                               time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

                        to_user_text = '''
一一一一 提现信息 一一一一

提现成功!
提现金额：%s 元
提现金额将以微信红包的形式发放，请耐心等待！
                                    ''' % (select_user_res[0][8])

                        itchat.send(to_user_text, msg['FromUserName'])
                        itchat.send(to_admin_text, '@e3eb58b811b064cdc2b3e544af64a55dcd87fb3824dcf307245c3cfe6f7f5036')

                        update_res = cm.ExecNonQuery(update_sql)
                        update_res = cm.ExecNonQuery(update_total_sql)
                        insert_current_log_res = cm.ExecNonQuery(insert_current_log_sql)

                        return
                    except Exception as e:
                        text = '''
一一一一 系统信息 一一一一

提现操作失败！已通知管理员，请耐心等待                        
                        '''
                        print(e)
                        itchat.send(text, msg['FromUserName'])
                        return
                else:
                    text = '''
一一一一 提现信息 一一一一

提现申请失败！

提现条件：
1，必须拥有个人账户，回复【10000】或者【邀请码】可创建个人账户并领取微信红包！
2，提现金额必须 >= 1元

把【淘口令】【京东商品链接】分享给我查询优惠券和返利！
使用教程：http://t.cn/RnAKqWW

回复【搜+商品名称】
回复【找+商品名称】
回复【买+商品名称】
可直接搜索淘宝京东所有优惠券！

tips：邀请好友也有返利哦亲！
戳我看详情： http://t.cn/RnAKafe
                            '''
                    itchat.send(text, msg['FromUserName'])
                    return
            elif pattern_profile.search(msg['Text']) != None:
                res = ishaveuserinfo(msg)

                if res['res'] == 'not_info':
                    itchat.send(res['text'], msg['FromUserName'])
                    return

                user_sql = "SELECT * FROM taojin_user_info WHERE wx_number='" + msg['FromUserName'] + "';"

                user_info = cm.ExecQuery(user_sql)

                if len(user_info) < 1:
                    send_text = '''
一一一一 个人信息 一一一一

你还没创建个人账户哦！

回复【邀请码】或【10000】创建个人账户哦!
还可以领取现金红包哦！

淘京机器人使用说明：
http://t.cn/RnAKqWW
                    '''
                    cm.Close()
                    itchat.send(text, msg['FromUserName'])
                    return

                current = "SELECT sum(amount) FROM taojin_current_log WHERE username=" + msg['FromUserName'] + ";"

                friends_count_sql = "SELECT count(*) FROM taojin_user_info WHERE lnivter='" + str(
                    user_info[0][4]) + "';"

                current_info = cm.ExecQuery(current)

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

总订单量: %s
京东订单量: %s
淘宝订单量: %s
好友返利: %s
好友个数: %s

您的邀请码是【%s】,赶快邀请好友领取奖励金吧，还有好友返利拿！
邀请详情：http://t.cn/RnAKafe
                                ''' % (
                    user_info[0][5], user_info[0][6], user_info[0][7], user_info[0][8], current_info, user_info[0][10],
                    user_info[0][11], user_info[0][12], user_info[0][18], friends_count[0][0], user_info[0][4])

                cm.Close()
                itchat.send(text, msg['FromUserName'])
                return
            elif pattern_tuig.search(msg['Text']) != None:
                res = ishaveuserinfo(msg)

                if res['res'] == 'not_info':
                    itchat.send(res['text'], msg['FromUserName'])
                    return

                user_sql = "SELECT * FROM taojin_user_info WHERE wx_number='" + msg['FromUserName'] + "';"

                user_info = cm.ExecQuery(user_sql)

                text = '''
一一一一 推广信息 一一一一

1,将机器人名片分享给您的好友
2,好友添加机器人为好友并回复您的邀请码【%s】

说明:好友添加机器人为好友，并输入您的专属邀请码，
您将获取0.3元现金红包奖励，并永久享受下级成功购物返利提成。

推广教程：http://t.cn/RnAKafe
    
                        ''' % (user_info[0][4])
                itchat.send(text, msg['FromUserName'])
            elif pattern_proxy.search(msg['Text']) != None:
                res = ishaveuserinfo(msg)

                if res['res'] == 'not_info':
                    itchat.send(res['text'], msg['FromUserName'])
                    return

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
一一一一 申请代理 一一一一

添加客服微信【18600611372】
备注验证：申请淘京机器人代理

客服人员将第一时间联系您！请耐心等待！
                        '''
                itchat.send(text, msg['FromUserName'])
                itchat.send(to_admin_text, '@30d4e21c638ab9bde3bdc57d4a46e0ae56aa00f2e40dca8ead787d9dc267223b')
            elif pattern_movie.search(msg['Text']) != None:
                pass
            elif (',' in msg['Text']) and (msg['Text'].split(',')[1].isdigit()) and (len(msg['Text'].split(',')[1]) == 11):
                res2 = ishaveuserinfo(msg)

                if res2['res'] == 'not_info':
                    itchat.send(res2['text'], msg['FromUserName'])
                    return

                res = mjd.get_jd_order(msg, msg['Text'].split(',')[0], msg['Text'].split(',')[1])

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
                    itchat.send('你当前没有个人账户请发送10000或邀请人的邀请码注册个人账户！', msg['FromUserName'])
                elif res['info'] == 'feild':

                    user_text = '''
一一一一订单信息一一一一

订单返利失败！

失败原因：
【1】未确认收货（打开App确认收货后重新发送）
【2】，当前商品不是通过机器人购买
【3】，查询格式不正确(正确格式：2018-03-20,73462222028 )
【4】，订单完成日期错误，请输入正确的订单查询日期
【6】，订单号错误，请输入正确的订单号

请按照提示进行重新操作！            
                                '''

                    itchat.send(user_text, msg['FromUserName'])
            elif ('，' in msg['Text']) and (msg['Text'].split('，')[1].isdigit()) and (len(msg['Text'].split('，')[1]) == 11):
                res2 = ishaveuserinfo(msg)

                if res2['res'] == 'not_info':
                    itchat.send(res2['text'], msg['FromUserName'])
                    return

                res = mjd.get_jd_order(msg, msg['Text'].split('，')[0], msg['Text'].split('，')[1])

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
                    itchat.send('你当前没有个人账户请发送10000或邀请人的邀请码注册个人账户！', msg['FromUserName'])
                elif res['info'] == 'feild':

                    user_text = '''
一一一一订单信息一一一一

订单返利失败！

失败原因：
【1】未确认收货（打开App确认收货后重新发送）
【2】，当前商品不是通过机器人购买
【3】，查询格式不正确(正确格式：2018-03-20,73462222028 )
【4】，订单完成日期错误，请输入正确的订单查询日期
【6】，订单号错误，请输入正确的订单号

请按照提示进行重新操作！            
                                '''

                    itchat.send(user_text, msg['FromUserName'])
            elif (',' in msg['Text']) and (msg['Text'].split(',')[1].isdigit()) and (len(msg['Text'].split(',')[1]) == 18):
                res2 = ishaveuserinfo(msg)

                if res2['res'] == 'not_info':
                    itchat.send(res2['text'], msg['FromUserName'])
                    return

                res = al.get_order(msg, msg['Text'].split(',')[0], msg['Text'].split(',')[1])

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
                    itchat.send('你当前没有个人账户请发送10000或邀请人的邀请码注册个人账户！', msg['FromUserName'])
                elif res['info'] == 'feild':
                    user_text = '''
一一一一订单信息一一一一

订单返利失败！

失败原因：
【1】未确认收货（打开App确认收货后重新发送）
【2】，当前商品不是通过机器人购买
【3】，查询格式不正确(正确格式：2018-03-20,73462222028 )
【4】，订单完成日期错误，请输入正确的订单查询日期
【6】，订单号错误，请输入正确的订单号

请按照提示进行重新操作！            
                                '''

                    itchat.send(user_text, msg['FromUserName'])
            elif ('，' in msg['Text']) and (msg['Text'].split('，')[1].isdigit()) and (len(msg['Text'].split('，')[1]) == 18):
                res2 = ishaveuserinfo(msg)

                if res2['res'] == 'not_info':
                    itchat.send(res2['text'], msg['FromUserName'])
                    return

                res = al.get_order(msg, msg['Text'].split('，')[0], msg['Text'].split('，')[1])

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
                    itchat.send('你当前没有个人账户请发送10000或邀请人的邀请码注册个人账户！', msg['FromUserName'])
                elif res['info'] == 'feild':
                    user_text = '''
一一一一订单信息一一一一

订单返利失败！

失败原因：
【1】未确认收货（打开App确认收货后重新发送）
【2】，当前商品不是通过机器人购买
【3】，查询格式不正确(正确格式：2018-03-20,73462222028 )
【4】，订单完成日期错误，请输入正确的订单查询日期
【6】，订单号错误，请输入正确的订单号

请按照提示进行重新操作！            
                                '''

                    itchat.send(user_text, msg['FromUserName'])
            else:
                msg_text = tuling(msg)
                itchat.send(msg_text, msg['FromUserName'])
                return
        else:
            res2 = ishaveuserinfo(msg)

            if res2['res'] == 'not_info':
                itchat.send(res2['text'], msg['FromUserName'])
                return

            text_reply(msg, msg['Text'])


# 创建用户账户
def create_user_info(msg, lnivt_code=0):
    cm = ConnectMysql()
    res = itchat.search_friends(userName=msg['RecommendInfo']['UserName'])
    while True:
        # 生成随机数
        randNum = random.randint(100000, 999999)

        # 定义SQL语句 查询数据是否已经存在
        select_sql = "SELECT * FROM taojin_user_info WHERE lnivt_code=" + str(randNum) + ""

        select_res = cm.ExecQuery(select_sql)

        if len(select_res) == 0:
            break

    # 定义SQL语句 查询数据是否已经存在
    select_user_sql = "SELECT * FROM taojin_user_info WHERE wx_number='" + res['UserName'] + "';"
    select_user_res = cm.ExecQuery(select_user_sql)
    if len(select_user_res) > 0:
        cm.Close()
        text = '''
一一一一 系统信息 一一一一

您已成功创建账户，请勿重新创建！

输入【余额】可查询账户余额信息
输入【帮助】可查询指信息
输入【提现】可申请账户余额提现
输入【推广】可申请机器人代理

淘京机器人使用说明：
http://t.cn/RnAKqWW
京东优惠券网站：
http://jdyhq.ptjob.net
淘宝优惠券网站：
http://tbyhq.ptjob.net
                '''
        itchat.send(text, msg['FromUserName'])
        return

    if lnivt_code == 0:
        sql = "INSERT INTO taojin_user_info(wx_number, sex, nickname, lnivt_code, withdrawals_amount, lnivter, create_time) VALUES('" + \
              res['UserName'] + "', '" + str(res['Sex']) + "', '" + res['NickName'] + "', '" + str(
            randNum) + "', '0.3', '" + str(lnivt_code) + "', '" + str(round(time.time())) + "');"

        insert_res = cm.ExecNonQuery(sql)

        if (insert_res):

            user_sql = "SELECT * FROM taojin_user_info WHERE wx_number='" + res['UserName'] + "' LIMIT 1;"

            current = "SELECT sum(amount) FROM taojin_current_log WHERE username=" + res['UserName'] + ";"

            user_info = cm.ExecQuery(user_sql)

            # 日志参数
            args = {
                'username': res['UserName'],
                'rebate_amount': 0.3,
                'type': 1,
                'create_time': time.time()
            }

            # 写入返利日志
            cm.InsertRebateLog(args)

            current_info = cm.ExecQuery(current)

            if current_info[0][0] == None:
                current_info = 0
            else:
                current_info = current_info[0][0]

            text = '''
一一一一 账户创建成功 一一一一

总返利金额:%s元
京东返利金额:%s元
淘宝返利金额:%s元
可提现余额:%s元
累计提现金额:%s元

总订单量:%s
京东订单量:%s
淘宝订单量:%s
好友个数:%s
好友返利:%s元

您的邀请码是【%s】,赶快邀请好友领取奖励金吧，还有好友返利拿！邀请详情：
http://t.cn/RnAKafe
                ''' % (
                user_info[0][5], user_info[0][6], user_info[0][7], user_info[0][8], current_info, user_info[0][10],
                user_info[0][11], user_info[0][12], user_info[0][18], user_info[0][19], user_info[0][4])

            cm.Close()
            itchat.send(text, msg['FromUserName'])
            return
    else:

        lnivter_sql = "SELECT * FROM taojin_user_info WHERE lnivt_code='" + lnivt_code + "' LIMIT 1;"

        # 获取邀请人信息
        lnivt_info = cm.ExecQuery(lnivter_sql)

        if len(lnivt_info) < 1:
            cm.Close()
            itchat.send('请发送有效的邀请码！', msg['FromUserName'])
            return

        # 有邀请人时，插入用户信息，并奖励邀请人
        sql = "INSERT INTO taojin_user_info(wx_number, sex, nickname, lnivt_code, withdrawals_amount, lnivter, create_time) VALUES('" + \
              res['UserName'] + "', '" + str(res['Sex']) + "', '" + res['NickName'] + "', '" + str(
            randNum) + "', '0.3', '" + str(lnivt_code) + "', '" + str(round(time.time())) + "');"

        # 给邀请人余额加0.3元奖励
        jianli = round(float(lnivt_info[0][8]) + 0.3, 2)

        friends_num = int(lnivt_info[0][19]) + 1

        lnivt_res = cm.ExecNonQuery("UPDATE taojin_user_info SET withdrawals_amount='" + str(
            jianli) + "', friends_number='" + str(friends_num) + "'  WHERE lnivt_code='" + lnivt_code + "';")

        insert_res = cm.ExecNonQuery(sql)

        # 日志参数
        args = {
            'username': res['UserName'],
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

        if (insert_res):

            user_sql = "SELECT * FROM taojin_user_info WHERE wx_number='" + res['UserName'] + "' LIMIT 1;"

            current = "SELECT sum(amount) FROM taojin_current_log WHERE username=" + res['UserName'] + ";"

            user_info = cm.ExecQuery(user_sql)

            current_info = cm.ExecQuery(current)

            if current_info[0][0] == None:
                current_info = 0
            else:
                current_info = current_info[0][0]

            text = '''

一一一一 系统消息 一一一一

账户创建成功！
账户开通奖励金0.3元已发放到您的账号
当前账户余额：%s元
回复【个人信息】查看账户信息
回复【帮助】可查询指令信息

您的邀请码为【%s】赶快邀请好友领取奖励金吧，还有好友返利拿！
邀请详情：http://t.cn/RnAKafe

                    ''' % (user_info[0][8], user_info[0][4])

            lnivt_text = '''
一一一一 推广消息 一一一一

微信好友【%s】通过邀请码已经绑定到你的账户
你将获取好友推广奖励金：0.3元
你将永久获得【%s】返利提成
当前可提现金额：%s 元
好友个数为 %s 个
            ''' % (user_info[0][3], user_info[0][3], jianli, friends_num)

            cm.Close()
            itchat.send(text, msg['FromUserName'])
            itchat.send(lnivt_text, lnivt_info[0][1])


# 使用邀请码创建账户, 或绑定邀请人
def lnivt_user(msg):
    cm = ConnectMysql()

    check_user_sql = "SELECT * FROM taojin_user_info WHERE wx_number='" + str(msg['FromUserName']) + "';"
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

账户创建失败：您已经有邀请人了！
请勿重新发送！
    `                   '''
            itchat.send(gg_text, msg['FromUserName'])
            return
        elif int(msg['Text']) == int(check_user_res[0][4]):
            cm.Close()
            gg_text = '''
一一一一系统消息一一一一

账户创建失败：邀请人不能是自己！
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
    `                   '''
            itchat.send(gg_text, msg['FromUserName'])
            return

        # 绑定邀请人
        add_lnivt_sql = "UPDATE taojin_user_info SET lnivter='" + str(msg['Text']) + "' WHERE wx_number='" + msg[
            'FromUserName'] + "';"

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

账户创建成功！
账户开通奖励金0.3元已发放到您的账号
当前账户余额：0.3元
回复【个人信息】查看账户信息
回复【帮助】可查询指令信息

您的邀请码为【%s】赶快邀请好友领取奖励金吧，还有好友返利拿！
邀请详情：http://t.cn/RnAKafe
                    ''' % (check_user_res[0][4])

            lnivt_text = '''
一一一一 推广消息 一一一一 

微信好友【%s】通过邀请码已经绑定到你的账户
你将获取好友推广奖励金：0.3元
你将永久获得【%s】返利提成
当前可提现金额：%s 元
好友个数为%s 个
            ''' % (check_user_res[0][3], check_user_res[0][3], jianli, friends_num)
            itchat.send(text, msg['FromUserName'])
            itchat.send(lnivt_text, lnivt_info[0][1])
        else:
            cm.Close()
            itchat.send('添加邀请人失败！请重试！', msg['FromUserName'])


# 判断用户是否有个人账户
def ishaveuserinfo(msg):
    cm = ConnectMysql()

    check_user_sql = "SELECT * FROM taojin_user_info WHERE wx_number='" + str(msg['FromUserName']) + "';"
    check_user_res = cm.ExecQuery(check_user_sql)

    # 判断是否已经有个人账户，没有去创建
    if len(check_user_res) < 1:
        cm.Close()
        send_text = '''
一一一一 个人信息 一一一一

你还没创建个人账户哦！

回复【邀请码】或【10000】创建个人账户哦!
还可以领取现金红包哦！

淘京机器人使用说明：
http://t.cn/RnAKqWW
                    '''
        return {"res": "not_info", "text": send_text}

    return {"res": "have_info"}


class WxBot(object):
    # 消息回复(文本类型和分享类型消息)
    @itchat.msg_register(['Text', 'Sharing'])
    def text(msg):
        print(msg)
        check_if_is_tb_link(msg)

    @itchat.msg_register(FRIENDS)
    def add_friend(msg):
        itchat.add_friend(**msg['Text'])  # 该操作会自动将新好友的消息录入，不需要重载通讯录
        create_user_info(msg)
        text = '''
一一一一 系统消息 一一一一

你好！欢迎使用跑堂优惠券！
先领券，再购物，更省钱！有返利！

回复【邀请码】或【10000】领取新人红包

回复【买+商品名称】
回复【找+商品名称】
回复【搜+商品名称】
查看商品优惠券合集

分享【京东商品链接】或者【淘口令】精准查询商品优惠券和返利信息！

优惠券使用教程：
http://t.cn/RnAKqWW
京东优惠券网站：
http://jdyhq.ptjob.net
淘宝优惠券网站：
http://tbyhq.ptjob.net
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
