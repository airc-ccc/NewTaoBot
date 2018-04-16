# -*- coding: UTF-8 -*-
# author Mr.Peng

import requests
import json
import time
import json
import platform
import re
import os
import webbrowser
import configparser
from selenium import webdriver
from bs4 import BeautifulSoup
from time import strftime,gmtime
from libs.mysql import ConnectMysql
from libs.wx_bot import *
from itchat.content import *
from libs.orther import Orther
from libs.tuling import tuling
from bottle import template

cookie_fname = 'cookies_jd.txt'
sysstr = platform.system()
config = configparser.ConfigParser()
config.read('config.conf', encoding="utf-8-sig")
ort = Orther()
tu = tuling()

class MediaJd:
    def __init__(self):
        self.se = requests.session()
        self.load_cookies()

    def getJd(self, msg, good_url):
        cm = ConnectMysql()
        print('开始查询分享商品的信息......', msg['Text'])

        wei_info = itchat.search_friends(userName=msg['FromUserName'])
        bot_info = itchat.search_friends(userName=msg['ToUserName'])

        sku_arr = good_url.split('https://item.m.jd.com/product/')

        if sku_arr == None:
            msg_text = tu.tuling(msg)
            print(msg_text)
            itchat.send(msg_text, msg['FromUserName'])
            return

        sku = sku_arr[1].split('.')

        res = self.get_good_link(sku[0])
        if res['data']['shotCouponUrl'] == '':
            text = '''
一一一一返利信息一一一一

【商品名】%s

【京东价】%s元
【返红包】%s元
 返利链接:%s

省钱步骤：
1,点击链接，进入下单！
2,订单完成后，将订单完成日期和订单号发给我哦！
例如：
2018-01-01,12345678901
                ''' % (res['logTitle'], res['logUnitPrice'], res['rebate'], res['data']['shotUrl'])
            itchat.send(text, msg['FromUserName'])

            insert_sql = "INSERT INTO taojin_query_record(wx_bot, good_title, good_price, good_coupon, username, create_time) VALUES('"+ bot_info['NickName'] +"', '" + \
                         res['logTitle'] + "', '" + str(res['logUnitPrice']) + "', '0', '" + wei_info[
                             'NickName'] + "', '" + str(time.time()) + "')"
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
                ''' % (
            res['logTitle'], res['logUnitPrice'], res['youhuiquan_price'], res['coupon_price'], res['rebate'],
            res['data']['shotCouponUrl'])

            insert_sql = "INSERT INTO taojin_query_record(wx_bot, good_title, good_price, good_coupon, username, create_time) VALUES('"+ bot_info['NickName'] +"', '" + \
                         res['logTitle'] + "', '" + str(res['logUnitPrice']) + "', '" + res['coupon_price2'] + "', '" + \
                         wei_info['NickName'] + "', '" + str(time.time()) + "')"
            cm.ExecNonQuery(insert_sql)

            itchat.send(text, msg['FromUserName'])
            return

    def getGroupJd(self, msg, good_url):
        cm = ConnectMysql()
        print('开始查询分享商品的信息......', msg['Text'])

        wei_info = itchat.search_chatrooms(userName=msg['FromUserName'])
        bot_info = itchat.search_chatrooms(userName=msg['ToUserName'])

        sku_arr = good_url.split('https://item.m.jd.com/product/')

        if sku_arr == None:
            msg_text = tu.tuling(msg)
            print(msg_text)
            itchat.send(msg_text, msg['FromUserName'])
            return

        sku = sku_arr[1].split('.')

        res = self.get_good_link(sku[0])
        logger.debug(res)
        if res['data']['shotCouponUrl'] == '':
            text = '''
一一一一返利信息一一一一

【商品名】%s

【京东价】%s元
 返利链接:%s
                ''' % (res['logTitle'], res['logUnitPrice'], res['data']['shotUrl'])
            itchat.send(text, msg['FromUserName'])

            insert_sql = "INSERT INTO taojin_query_record(wx_bot, good_title, good_price, good_coupon, username, create_time) VALUES('"+ bot_info['NickName'] +"', '" + \
                         res['logTitle'] + "', '" + str(res['logUnitPrice']) + "', '0', '" + wei_info[
                             'NickName'] + "', '" + str(time.time()) + "')"
            cm.ExecNonQuery(insert_sql)
            return
        else:
            text = '''
一一一一返利信息一一一一

【商品名】%s

【京东价】%s元
【优惠券】%s元
【券后价】%s元
 领券链接:%s
                ''' % (
            res['logTitle'], res['logUnitPrice'], res['youhuiquan_price'], res['coupon_price'],
            res['data']['shotCouponUrl'])

            insert_sql = "INSERT INTO taojin_query_record(wx_bot, good_title, good_price, good_coupon, username, create_time) VALUES('"+ bot_info['NickName'] +"', '" + \
                         res['logTitle'] + "', '" + str(res['logUnitPrice']) + "', '" + res['coupon_price2'] + "', '" + \
                         wei_info['NickName'] + "', '" + str(time.time()) + "')"
            cm.ExecNonQuery(insert_sql)

            itchat.send(text, msg['FromUserName'])
            return

    def check_login(self):

        self.load_cookies()

        url = 'https://media.jd.com/gotoadv/goods?pageSize=50'

        res = self.se.get(url)

        # 使用BeautifulSoup解析HTML，并提取登录属性，判断登录是否失效
        soup = BeautifulSoup(res.text, 'lxml')

        login = soup.select('.tips')

        # 判断登录状态是否失效
        if len(login) > 0:
            return 'Login Failed'
        else:
            return 'Login Success'

    def do_login(self):
        #loginname = input('请输入京东联盟账号:')
        #nloginpwd = input('请输入京东联盟密码:')

        if (sysstr == "Linux") or (sysstr == "Darwin"):
            firefoxOptions = webdriver.FirefoxOptions()

            firefoxOptions.set_headless()

            # 开启driver
            wd = webdriver.Firefox(firefox_options=firefoxOptions)
        else:
            wd = webdriver.Firefox()
        wd.get('https://passport.jd.com/common/loginPage?from=media&ReturnUrl=https%3A%2F%2Fmedia.jd.com%2FloginJump')
        # 输入账号密码
        wd.find_element_by_id('loginname').send_keys(config.get('JD', 'JD_USERNAME'))
        # 休息3秒
        time.sleep(3)
        # 输入密码
        wd.find_element_by_id('nloginpwd').send_keys(config.get('JD', 'JD_PASSWORD'))
        # 点击登录按钮
        time.sleep(10)
        wd.find_element_by_id('paipaiLoginSubmit').click()
        # 获取cookie并写入文件
        cookies = wd.get_cookies()
        # 写入Cookies文件
        with open(cookie_fname, 'w') as f:
            f.write(json.dumps(cookies))

        return 'Login Success'

    def login(self):
        clr = self.check_login()
        if 'Login Success' in clr:
            print('京东已登录！不需要再次登录！')
            return 'Login Success'
        else:
            self.do_login()

    def load_cookies(self):
        if os.path.isfile(cookie_fname):
            with open(cookie_fname, 'r') as f:
                c_str = f.read().strip()
                self.set_cookies(c_str)

    def set_cookies(self, c_str):
        try:
            cookies = json.loads(c_str)
        except:
            return
        for c in cookies:
            self.se.cookies.set(c['name'], c['value'])

    def get_good_link(self, good_name):
        self.load_cookies()
        uu = "https://media.jd.com/gotoadv/goods?searchId=2011016742%23%23%23st1%23%23%23kt1%23%23%23598e10defb7f41debe6af038e875b61c&pageIndex=&pageSize=50&property=&sort=&goodsView=&adownerType=&pcRate=&wlRate=&category1=&category=&category3=&condition=0&fromPrice=&toPrice=&dataFlag=0&keyword='" + good_name + "'&input_keyword='" + good_name + "'&price=PC"
        # 搜索商品
        res = self.se.get(uu)

        # 使用BeautifulSoup解析HTML，并提取属性数据
        soup = BeautifulSoup(res.text, 'lxml')

        a = soup.select('.extension-btn')

        coupon = soup.find(attrs={'style':'color: #ff5400;'})

        coupon_price = 0;

        if coupon != None:
            coupon_text = coupon.string

            coupon_price = coupon_text.split('减')[1]


        request_id = soup.select('#requestId')

        str_onclick = a[0].get('onclick')

        string = str_onclick[13:-8]

        arr = string.split(',')

        dict_str = {}

        for item in arr:
            str = item.split('\':')
            str_b = str[0].split('\r\n\t\t\t\t\t\t\t')
            str_1 = str_b[1].strip()
            str_2 = str_1.split('\'')
            str_3 = str[1].split('\'')

            if len(str_3) >= 2:
                dict_str[str_2[1]] = str_3[1]
            else:
                dict_str[str_2[1]] = str_3[0]

        # 拼装FormData
        dict_str['adtType'] = 31
        dict_str['siteName'] = -1
        dict_str['unionWebId'] = -1
        dict_str['protocol'] = 1
        dict_str['codeType'] = 2
        dict_str['type'] = 1
        dict_str['positionId'] = config.get('JD', 'JD_POSITION_ID')
        dict_str['positionName'] = config.get('JD', 'JD_POSITION_NAME')
        dict_str['sizeId'] = -1
        dict_str['logSizeName'] = -1
        dict_str['unionAppId'] = -1
        dict_str['unionMediaId'] = -1
        dict_str['materialType'] = 1
        dict_str['orienPlanId'] = -1
        dict_str['landingPageType'] = -1
        dict_str['adOwner'] = 'z_0'
        dict_str['saler'] = -1
        dict_str['isApp'] = -1
        dict_str['actId'] = dict_str['materialId']
        dict_str['wareUrl'] = dict_str['pcDetails']
        dict_str['category'] = dict_str['logCategory']
        dict_str['requestId'] = request_id[0].get('value')

        # 删除多余的属性
        dict_str.pop('logCategory')
        dict_str.pop('pcDetails')
        dict_str.pop('mDetails')

        # 获取领券链接和下单链接
        good_link = self.se.post('https://media.jd.com/gotoadv/getCustomCodeURL', data=dict_str)

        good_text = json.loads(good_link.text)
        good_text['logTitle'] = dict_str['logTitle']
        good_text['logUnitPrice'] = dict_str['logUnitPrice']
        good_text['imgUrl'] = dict_str['imgUrl']
        rebate = float(dict_str['pcComm']) / 100
        if coupon != None:
            good_text['coupon_price'] = round(float(good_text['logUnitPrice']) - int(coupon_price), 2)
            good_text['youhuiquan_price'] = coupon_price
            good_text['rebate'] = round(float(good_text['coupon_price']) * rebate * 0.3, 2)
        else:
            good_text['rebate'] = round(float(good_text['logUnitPrice']) * rebate * 0.3, 2)

        good_text['coupon_price2'] = coupon_price
        return good_text


    # 随机获取商品信息
    def get_good_info(self, wx_bot):
        cm = ConnectMysql()
        self.load_cookies()
        page = 1
        sku_num = 0
        print('aaa')
        while sku_num < 20:
            url = "https://media.jd.com/gotoadv/goods?searchId=2011005331%23%23%23st3%23%23%23kt0%23%23%2378dc30b6-fa14-4c67-900c-235b129ab4bb&pageIndex="+str(page)+"&pageSize=50&property=&sort=&goodsView=&adownerType=&pcRate=&wlRate=&category1=&category=&category3=&condition=1&fromPrice=&toPrice=&dataFlag=0&keyword=&input_keyword=&hasCoupon=1&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC&price=PC"
            page += 1
            print(page)
            res = self.se.get(url)
            soup = BeautifulSoup(res.text, 'lxml')
            skuList = []
            for li in soup.find_all('li', skuid = re.compile('^[0-9]+$')):
                sku = li.get('skuid')

                exists_sql = "SELECT * FROM taojin_good_info WHERE skuid='"+str(sku)+"' AND wx_bot='"+ wx_bot +"';"
                is_exists = cm.ExecQuery(exists_sql)
                if len(is_exists) != 0:
                    print('0....')
                    continue

                sku_num += 1
                skuList.append(sku)

            if skuList == []:
                print('[]....')
                continue

            for item in skuList:
                link_info = self.get_good_link(str(item))
                # item_image = link_info['data']['qRcode']
                item_image = link_info['imgUrl']
                # 请求图片
                res_img = requests.get(item_image)
                img_name = item_image.split('/')
                # 拼接图片名
                file_name = "images/" + img_name[-1]
                fp = open(file_name, 'wb')
                # 写入图片
                fp.write(res_img.content)
                fp.close()
                if link_info['data']['shotCouponUrl'] == '':
                    continue
                else:
                    sql = "INSERT INTO taojin_good_info(wx_bot, skuid, title, image, price, rebate, yhq_price, coupon_price, shoturl, shotcouponurl, status, create_time) VALUES('"+ wx_bot +"', '" + str(
                        item) + "', '" + str(link_info['logTitle']) + "', '" + str(item_image) + "', '" + str(
                        link_info['logUnitPrice']) + "', '" + str(link_info['rebate']) + "', '" + str(
                        link_info['youhuiquan_price']) + "', '" + str(link_info['coupon_price']) + "', '" + str(
                        link_info['data']['shotUrl']) + "', '" + str(
                        link_info['data']['shotCouponUrl']) + "', '1', '" + str(time.time()) + "')"

                cm.ExecNonQuery(sql)

        print("insert success!")


    def get_jd_order(self, msg, times, orderId, userInfo):
        # try:

        timestr = re.sub('-', '', times)
        order_id = int(orderId)

        cm = ConnectMysql()

        bot_info = itchat.search_friends(userName=msg['ToUserName'])

        # 查询订单是否已经提现过了
        check_order_sql = "SELECT * FROM taojin_order WHERE order_id='" + str(order_id) + "' AND wx_bot='"+ bot_info['NickName'] +"';"
        check_order_res = cm.ExecQuery(check_order_sql)

        # 判断该订单是否已经提现
        if len(check_order_res) >= 1:
            cm.Close()
            send_text = '''
一一一一 订单消息 一一一一

订单【%s】已经成功返利，请勿重复提交订单信息！
回复【个人信息】 查看订单及返利信息
如有疑问！请联系管理员
                        ''' % (order_id)
            return {"info": "order_exit", "send_text": send_text}

        self.load_cookies()

        url = 'https://api.jd.com/routerjson?v=2.0&method=jingdong.UnionService.queryOrderList&app_key=96432331E3ACE521CC0D66246EB4C371&access_token=a67c6103-691c-4691-92a2-4dee41ce0f88&360buy_param_json={"unionId":"2011005331","time":"'+timestr+'","pageIndex":"1","pageSize":"50"}&timestamp='+strftime("%Y-%m-%d %H:%M:%S", gmtime())+'&sign=E9D115D4769BDF68FE1DF07D33F7720B'
        print(url)
        res = requests.get(url)

        rj = json.loads(res.text)
        print(rj, url)
        data = json.loads(rj['jingdong_UnionService_queryOrderList_responce']['result'])

        for item in data['data']:
            if int(order_id) == int(item['orderId']):
                res = self.changeInfo(msg, item, order_id, userInfo, timestr)
                return res

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

        return {'info': 'not_order', 'user_text': user_text}
        # except Exception as e:
        #     print(e)
        #     return {'info': 'feild'}

    def changeInfo(self, msg, info, order_id, userInfo, timestr):

        cm = ConnectMysql()
        # try:
        bot_info = itchat.search_friends(userName=msg['ToUserName'])
        # 查询用户是否有上线
        check_user_sql = "SELECT * FROM taojin_user_info WHERE wx_number='" + str(userInfo['NickName']) + "' AND wx_bot='"+ bot_info['NickName'] +"';"
        check_user_res = cm.ExecQuery(check_user_sql)

        # 判断是否已经有个人账户，没有返回信息
        if len(check_user_res) < 1:
            cm.Close()
            return {"info": "not_info"}
        else:
            get_query_sql = "SELECT * FROM taojin_query_record WHERE good_title='" + info['skuList'][0]['skuName'] + "'AND username='" + check_user_res[0][2] + "' AND wx_bot='"+ bot_info['NickName'] +"' ORDER BY create_time LIMIT 1;"

            get_query_info = cm.ExecQuery(get_query_sql)

            if get_query_info == ():
                user_text = '''
一一一一订单信息一一一一

订单返利失败！

失败原因：当前商品不是通过当前机器人购买

请按照提示进行重新操作！
                '''
                return {'info': 'not_order', 'user_text': user_text}

            # 定义SQL语句 查询用户是否已经存在邀请人
            # 判断是否已经有邀请人了
            if check_user_res.isdigit() and int(check_user_res[0][17]) != 0:

                get_parent_sql = "SELECT * FROM taojin_user_info WHERE lnivt_code='" + str(
                    check_user_res[0][17]) + "' AND wx_bot='"+ bot_info['NickName'] +"';"

                get_parent_info = cm.ExecQuery(get_parent_sql)

                # 计算返利金额
                add_balance = round(float(info['skuList'][0]['actualFee']) * 0.3, 2)
                # 累加宗金额
                withdrawals_amount = round(float(check_user_res[0][9]) + add_balance, 2)
                # 计算京东返利金额
                jd = round(float(check_user_res[0][7]) + add_balance, 2)
                # 计算总返利金额
                total_rebate_amount = round(float(check_user_res[0][6]) + add_balance, 2)
                
                jishen = round(float(get_query_info[0][3]) - float(info['skuList'][0]['payPrice']))

                if jishen < 0:
                    jishen = 0

                # 计算总节省金额
                save_money = round(
                    check_user_res[0][10] + jishen, 2)

                add_parent_balance = round(float(info['skuList'][0]['actualFee']) * 0.1, 2)
                withdrawals_amount2 = round(float(get_parent_info[0][9]) + float(add_balance) * 0.1, 2)

                # 订单数加1
                # 总订单数加一
                total_order_num = int(check_user_res[0][11]) + 1
                # 订单数加一
                jd_order_num = int(check_user_res[0][12]) + 1

                cm.ExecNonQuery("UPDATE taojin_user_info SET withdrawals_amount='" + str(withdrawals_amount) + "', save_money='" + str(save_money) + "', jd_rebate_amount='" + str(jd) + "', total_rebate_amount='" + str(total_rebate_amount) + "', update_time='" + str(time.time()) + "', order_quantity='"+str(total_order_num)+"', jd_order_quantity='"+str(jd_order_num)+"' WHERE wx_number='" + str(userInfo['NickName']) + "' AND wx_bot='"+ bot_info['NickName'] +"';")
                cm.ExecNonQuery("UPDATE taojin_user_info SET withdrawals_amount='" + str(withdrawals_amount2) + "', friends_rebate='"+str(add_parent_balance)+"', update_time='" + str(time.time()) + "' WHERE lnivt_code='" + str(check_user_res[0][17]) + "';")

                cm.ExecNonQuery("INSERT INTO taojin_order(wx_bot, username, order_id, completion_time, order_source) VALUES('"+ str(bot_info['NickName']) +"', '" + str(userInfo['NickName']) + "', '" + str(order_id) + "', '" + str(timestr) + "', '1')")

                args = {
                    'wx_bot': bot_info['NickName'],
                    'username': check_user_res[0][2],
                    'rebate_amount': add_balance,
                    'type': 3,
                    'create_time': time.time()
                }


                # 写入返利日志
                cm.InsertRebateLog(args)

                args2 = {
                    'wx_bot': bot_info['NickName'],
                    'username': get_parent_info[0][2],
                    'rebate_amount': add_parent_balance,
                    'type': 4,
                    'create_time': time.time()
                }


                # 写入返利日志
                cm.InsertRebateLog(args2)

                parent_user_text = '''
一一一一  推广信息 一一一一

您的好友【%s】又完成了一笔订单，返利提成%s元已发放到您的账户
回复【个人信息】查询账户信息及提成
                        ''' % (check_user_res[0][2], add_parent_balance)

                user_text = '''
一一一一系统消息一一一一

订单【%s】已完成！
返利金%s元已发放到您的个人账户！

                        ''' % (order_id, add_balance)
                cm.Close()
                return {'parent_user_text': parent_user_text, 'user_text': user_text, 'info': 'success',
                        'parent': get_parent_info[0][2]}
            else:
                add_balance = round(float(info['skuList'][0]['actualFee']) * 0.3, 2)
                print(info, add_balance)
                withdrawals_amount = round(float(check_user_res[0][9]) + add_balance, 2)
                jd = round(float(check_user_res[0][7]) + add_balance, 2)
                total_rebate_amount = round(float(check_user_res[0][6]) + add_balance, 2)

                jishen = round(float(get_query_info[0][3]) - float(info['skuList'][0]['payPrice']))

                if jishen < 0:
                    jishen = 0
                save_money = round(check_user_res[0][10] + jishen, 2)

                # 订单数加1
                # 总订单数加一
                total_order_num = int(check_user_res[0][11]) + 1
                # 订单数加一
                jd_order_num = int(check_user_res[0][12]) + 1

                up_sql = "UPDATE taojin_user_info SET jd_rebate_amount='" + str(jd) + "', withdrawals_amount='" + str(withdrawals_amount) + "', save_money='" + str(save_money) + "', total_rebate_amount='" + str(total_rebate_amount) + "', update_time='" + str(time.time()) + "', order_quantity='"+str(total_order_num)+"', jd_order_quantity='"+str(jd_order_num)+"' WHERE wx_number='" + str(userInfo['NickName']) + "' AND wx_bot='"+ bot_info['NickName'] +"';"
                print(up_sql)
                cm.ExecNonQuery(up_sql)
                cm.ExecNonQuery("INSERT INTO taojin_order(wx_bot, username, order_id, completion_time, order_source) VALUES('"+ bot_info['NickName'] +"', '" + str(userInfo['NickName']) + "', '" + str(order_id) + "', '" + str(timestr) + "', '2')")

                args = {
                    'wx_bot': bot_info['NickName'],
                    'username': check_user_res[0][2],
                    'rebate_amount': add_balance,
                    'type': 3,
                    'create_time': time.time()
                }


                # 写入返利日志
                cm.InsertRebateLog(args)

                user_text = '''
一一一一 订单消息 一一一一

订单【%s】标记成功，返利金%s已发放到您的账户
回复【个人信息】 查看订单及返利信息
                            ''' % (order_id, add_balance)
                cm.Close()
                return {'user_text': user_text, 'info': 'not_parent_and_success'}
        # except Exception as e:
        #     print(e)
        #     return {'info': 'feild'}




