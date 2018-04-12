# encoding: utf-8

import json
import os.path
import platform
import re
import sys
import time
import traceback
import itchat
import requests
import random
import datetime

if sys.version_info[0] < 3:
    import urllib
else:
    import urllib.parse as urllib
    
from io import BytesIO
from threading import Thread
from dateutil.relativedelta import relativedelta
from libs.mysql import ConnectMysql
from libs.wx_bot import *
from itchat.content import *
from libs.mediaJd import MediaJd
from libs.orther import Orther
from selenium import webdriver

import pyqrcode
import requests

from PIL import Image

sysstr = platform.system()
if (sysstr == "Linux") or (sysstr == "Darwin"):
    pass
cookie_fname = 'cookies_taobao.txt'


ort = Orther()

class Alimama:
    def __init__(self, logger):
        self.se = requests.session()
        self.load_cookies()
        self.myip = "127.0.0.1"
        self.start_keep_cookie_thread()
        self.logger = logger


    def getTao(self, msg):
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

            real_url = self.get_real_url(url)

            res = self.get_detail(real_url, msg)
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
            price = res['zkPrice']
            fx2 = round(float(res['tkCommonFee']) * 0.3, 2)
            real_price = round(price - coupon_amount, 2)
            res1 = self.get_tk_link(auctionid)

            if res1 == None:
                img = self.get_qr_image()
                itchat.send(img, msg['FromUserName'])
                return
            tao_token = res1['taoToken']
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
            self.logger.warning("error:{},trace:{}".format(str(e), trace))
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

    def getGroupTao(self, msg):
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

            real_url = self.get_real_url(url)

            res = self.get_group_detail(real_url, msg)
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
                                '''
                itchat.send(text, msg['FromUserName'])
                return

            auctionid = res['auctionId']
            coupon_amount = res['couponAmount']
            price = res['zkPrice']
            fx2 = round(float(res['tkCommonFee']) * 0.3, 2)
            real_price = round(price - coupon_amount, 2)
            res1 = self.get_tk_link(auctionid)

            if res1 == None:
                img = self.get_qr_image()
                itchat.send(img, msg['FromUserName'])
                return
            tao_token = res1['taoToken']
            coupon_link = res1['couponLink']
            if coupon_link != "":
                coupon_token = res1['couponLinkTaoToken']
                res_text = '''
一一一一返利信息一一一一

【商品名】%s元

【淘宝价】%s元
【优惠券】%s元
【券后价】%s元
【淘口令】%s

 复制本条消息，打开淘宝App领取优惠券！
                        ''' % (q, price, coupon_amount, real_price, coupon_token)
            else:
                res_text = '''
一一一一返利信息一一一一

【商品名】%s
【淘宝价】%s元
【淘口令】%s
 复制本条消息
                                        ''' % (q, price, tao_token)

            itchat.send(res_text, msg['FromUserName'])
        except Exception as e:
            trace = traceback.format_exc()
            self.logger.warning("error:{},trace:{}".format(str(e), trace))
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
                    '''
            itchat.send(info, msg['FromUserName'])

    # 启动一个线程，定时访问淘宝联盟主页，防止cookie失效
    def start_keep_cookie_thread(self):
        t = Thread(target=self.visit_main_url, args=())
        t.setDaemon(True)
        t.start()

    def visit_main_url(self):
        url = "https://pub.alimama.com/"
        headers = {
            'method': 'GET',
            'authority': 'pub.alimama.com',
            'scheme': 'https',
            'path': '/common/getUnionPubContextInfo.json',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            'Referer': 'http://pub.alimama.com/',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2',
        }
        while True:
            time.sleep(60 * 5)
            try:
                self.logger.debug("visit_main_url......,time:{}".format(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())))
                self.get_url(url, headers)
                self.logger.debug(self.check_login())
                real_url = "https://detail.tmall.com/item.htm?id=42485910384"
                res = self.get_detail2(real_url)
                auctionid = res['auctionId']
                self.logger.debug(self.get_tk_link(auctionid))
            except Exception as e:
                trace = traceback.format_exc()
                self.logger.warning("error:{},trace:{}".format(str(e), trace))

    # 获取商品详情
    def get_detail2(self, q):
        cm = ConnectMysql()
        try:
            t = int(time.time() * 1000)
            tb_token = self.se.cookies.get('_tb_token_', domain="pub.alimama.com")
            pvid = '10_%s_1686_%s' % (self.myip, t)
            url = 'http://pub.alimama.com/items/search.json?q=%s&_t=%s&auctionTag=&perPageSize=40&shopTag=&t=%s&_tb_token_=%s&pvid=%s' % (
                urllib.quote(q.encode('utf8')), t, t, tb_token, pvid)
            headers = {
                'method': 'GET',
                'authority': 'pub.alimama.com',
                'scheme': 'https',
                'path': '/items/search.json?%s' % url.split('search.json?')[-1],
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'x-requested-with': 'XMLHttpRequest',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
                'referer': 'https://pub.alimama.com',
                'accept-encoding': 'gzip, deflate, sdch, br',
                'accept-language': 'zh,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2',
            }
            res = self.get_url(url, headers)
            rj = res.json()
            if rj['data']['pageList'] != None:
                return rj['data']['pageList'][0]
            else:
                return 'no match item'
        except Exception as e:
            trace = traceback.format_exc()
            self.logger.warning("error:{},trace:{}".format(str(e), trace))

    def get_url(self, url, headers):
        res = self.se.get(url, headers=headers)
        return res

    def post_url(self, url, headers, data):
        res = self.se.post(url, headers=headers, data=data)
        return res

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
            self.se.cookies.set(c[0], c[1])

    # check login
    def check_login(self):
        # self.logger.debug('checking login status.....')
        url = 'https://pub.alimama.com/common/getUnionPubContextInfo.json'
        headers = {
            'method': 'GET',
            'authority': 'pub.alimama.com',
            'scheme': 'https',
            'path': '/common/getUnionPubContextInfo.json',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            'Referer': 'http://pub.alimama.com/',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2',
        }

        res = self.get_url(url, headers=headers)
        rj = json.loads(res.text)
        return rj

    def visit_login_rediret_url(self, url):
        headers = {
            'method': 'GET',
            'authority': 'login.taobao.com',
            'scheme': 'https',
            'path': '/member/loginByIm.do?%s' % url.split('loginByIm.do?')[-1],
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            'Referer': 'http://pub.alimama.com/',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2',
        }
        res = self.get_url(url, headers=headers)
        self.logger.debug(res.status_code)

    def get_scan_qr_status(self, lg_token):
        defaulturl = 'http://login.taobao.com/member/taobaoke/login.htm?is_login=1'
        url = 'https://qrlogin.taobao.com/qrcodelogin/qrcodeLoginCheck.do?lgToken=%s&defaulturl=%s&_ksTS=%s_30&callback=jsonp31' % (
            lg_token, defaulturl, int(time.time() * 1000))
        headers = {
            'method': 'GET',
            'authority': 'qrlogin.taobao.com',
            'scheme': 'https',
            'path': '/qrcodelogin/qrcodeLoginCheck.do?%s' % url.split('qrcodeLoginCheck.do?')[-1],
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            'accept': '*/*',
            'referer': 'https://login.taobao.com/member/login.jhtml?style=mini&newMini2=true&from=alimama&redirectURL=http%3A%2F%2Flogin.taobao.com%2Fmember%2Ftaobaoke%2Flogin.htm%3Fis_login%3d1&full_redirect=true&disableQuickLogin=true',
            'accept-encoding': 'gzip, deflate, sdch, br',
            'accept-language': 'zh,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2',
        }
        res = self.get_url(url, headers=headers)
        rj = json.loads(res.text.replace('(function(){jsonp31(', '').replace(');})();', ''))
        return rj

    def show_qr_image(self):
        self.logger.debug('begin to show qr image')
        url = 'https://qrlogin.taobao.com/qrcodelogin/generateQRCode4Login.do?from=alimama&_ksTS=%s_30&callback=jsonp31' % int(
            time.time() * 1000)
        
        # get qr image
        headers = {
            'method': 'GET',
            'authority': 'qrlogin.taobao.com',
            'scheme': 'https',
            'path': '/qrcodelogin/generateQRCode4Login.do?%s' % url.split('generateQRCode4Login.do?')[-1],
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            'accept': '*/*',
            'referer': 'https://login.taobao.com/member/login.jhtml?style=mini&newMini2=true&from=alimama&redirectURL=http%3A%2F%2Flogin.taobao.com%2Fmember%2Ftaobaoke%2Flogin.htm%3Fis_login%3d1&full_redirect=true&disableQuickLogin=true',
            'accept-encoding': 'gzip, deflate, sdch, br',
            'accept-language': 'zh-CN,zh;q=0.8',
        }

        res = self.get_url(url, headers=headers)
        rj = json.loads(res.text.replace('(function(){jsonp31(', '').replace(');})();', ''))
        lg_token = rj['lgToken']
        url = 'https:%s' % rj['url']

        headers = {
            'method': 'GET',
            'authority': 'img.alicdn.com',
            'scheme': 'https',
            'path': '/tfscom/%s' % url.split('tfscom/')[-1],
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            'accept': 'image/webp,image/*,*/*;q=0.8',
            'referer': 'https://login.taobao.com/member/login.jhtml?style=mini&newMini2=true&from=alimama&redirectURL=http%3A%2F%2Flogin.taobao.com%2Fmember%2Ftaobaoke%2Flogin.htm%3Fis_login%3d1&full_redirect=true&disableQuickLogin=true',
            'accept-encoding': 'gzip, deflate, sdch, br',
            'accept-language': 'zh,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2',
        }
        res = self.get_url(url, headers=headers)
        qrimg = BytesIO(res.content)
        self.logger.debug(u"begin qr")
        
        sysstr = platform.system()
        if (sysstr == "Windows"):
            # windows下可能无法打印请用下列代码
            img = Image.open(qrimg)
            img.show()
        
        elif (sysstr == "Linux") or (sysstr == "Darwin"):
            # 读取url
            import zbarlight
            img = Image.open(qrimg)
            codes = zbarlight.scan_codes('qrcode', img)
            qr_url = codes[0]
            # 使用pyqrcode在终端打印，只在linux下可以用
            pyqrcode_url = pyqrcode.create(qr_url)
            print (pyqrcode_url.terminal())

        self.logger.debug(u"请使用淘宝客户端扫码")
        return lg_token

    def get_qr_image(self):
        url = 'https://qrlogin.taobao.com/qrcodelogin/generateQRCode4Login.do?from=alimama&_ksTS=%s_30&callback=jsonp31' % int(
            time.time() * 1000)

        # get qr image
        headers = {
            'method': 'GET',
            'authority': 'qrlogin.taobao.com',
            'scheme': 'https',
            'path': '/qrcodelogin/generateQRCode4Login.do?%s' % url.split('generateQRCode4Login.do?')[-1],
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            'accept': '*/*',
            'referer': 'https://login.taobao.com/member/login.jhtml?style=mini&newMini2=true&from=alimama&redirectURL=http%3A%2F%2Flogin.taobao.com%2Fmember%2Ftaobaoke%2Flogin.htm%3Fis_login%3d1&full_redirect=true&disableQuickLogin=true',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh-CN,zh;q=0.8',
        }

        res = self.get_url(url, headers=headers)
        rj = json.loads(res.text.replace('(function(){jsonp31(', '').replace(');})();', ''))
        lg_token = rj['lgToken']
        url = 'https:%s' % rj['url']

        headers = {
            'method': 'GET',
            'authority': 'img.alicdn.com',
            'scheme': 'https',
            'path': '/tfscom/%s' % url.split('tfscom/')[-1],
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            'accept': 'image/webp,image/*,*/*;q=0.8',
            'referer': 'https://login.taobao.com/member/login.jhtml?style=mini&newMini2=true&from=alimama&redirectURL=http%3A%2F%2Flogin.taobao.com%2Fmember%2Ftaobaoke%2Flogin.htm%3Fis_login%3d1&full_redirect=true&disableQuickLogin=true',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'zh,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2',
        }
        res = self.get_url(url, headers=headers)
        qrimg = BytesIO(res.content)
        self.logger.debug("TaoBao Login Out!")
        return qrimg


    # do login
    def do_login(self):
        self.logger.debug('begin to login')
        # show qr image
        lg_token = self.show_qr_image()
        t0 = time.time()
        while True:
            rj = self.get_scan_qr_status(lg_token)
            # 扫码成功会有跳转
            if 'url' in rj:
                self.visit_login_rediret_url(rj['url'])
                self.logger.debug('login success')
                # self.logger.debug(self.se.cookies)
                with open(cookie_fname, 'w') as f:
                    f.write(json.dumps(self.se.cookies.items()))
                return 'login success'
            # 二维码过一段时间会失效
            if time.time() - t0 > 60 * 5:
                self.logger.debug('scan timeout')
                return
            time.sleep(0.5)

    def login(self):
        try:
            clr = self.check_login()
            self.myip = clr['data']['ip']
            if 'mmNick' in clr['data']:
                self.logger.debug(u"淘宝已经登录 不需要再次登录")
                return 'login success'
            else:
                dlr = self.open_do_login()
                if dlr is None:
                    return 'login failed'
                else:
                    return 'login success'
        except Exception as e:
            trace = traceback.format_exc()
            self.logger.warning("{},{}".format(str(e), trace))
            return 'login failed'

    def open_do_login(self):
        loginname = input('请输入淘宝联盟账号:')
        nloginpwd = input('请输入淘宝联盟密码:')

        if (sysstr == "Linux") or (sysstr == "Darwin"):
            firefoxOptions = webdriver.FirefoxOptions()

            firefoxOptions.set_headless()

            # 开启driver
            wd = webdriver.Firefox(firefox_options=firefoxOptions)
        else:
            wd = webdriver.Firefox()

        wd.get('https://login.taobao.com/member/login.jhtml?style=mini&newMini2=true&from=alimama&redirectURL=http://login.taobao.com/member/taobaoke/login.htm?is_login=1&full_redirect=true&disableQuickLogin=true')

        time.sleep(10)

        js = "var pass = document.getElementById(\"TPL_password_1\").setAttribute(\"autocomplete\", \"on\")"

        wd.execute_script(js)
        time.sleep(3)
        wd.find_element_by_class_name('login-switch').click()
        time.sleep(3)
        # 输入账号密码
        wd.find_element_by_id('TPL_username_1').send_keys(loginname)
        # 休息3秒
        time.sleep(3)
        # 输入密码
        wd.find_element_by_id('TPL_password_1').send_keys(nloginpwd)
        # 点击登录按钮
        time.sleep(5)
        wd.find_element_by_id('J_SubmitStatic').click()

        self.logger.debug('login success')
        with open(cookie_fname, 'w') as f:
            cookies_arr = []
            for item in wd.get_cookies():
                cookies_arr.append([item['name'], item['value']])
            
            f.write(json.dumps(cookies_arr))
        # wd.close()
        return 'login success'

    def get_tb_token(self):
        tb_token = None
        for c in self.se.cookies.items():
            if c[0] == '_tb_token_':
                return c[1]
        if tb_token is None:
            return 'test'

    # 获取商品详情
    def get_detail(self, q, msg):
        cm = ConnectMysql()

        userInfo = itchat.search_friends(userName=msg['FromUserName'])
        bot_info = itchat.search_friends(userName=msg['ToUserName'])

        try:
            t = int(time.time() * 1000)
            tb_token = self.se.cookies.get('_tb_token_', domain="pub.alimama.com")
            pvid = '10_%s_1686_%s' % (self.myip, t)
            url = 'http://pub.alimama.com/items/search.json?q=%s&_t=%s&auctionTag=&perPageSize=40&shopTag=&t=%s&_tb_token_=%s&pvid=%s' % (
                urllib.quote(q.encode('utf8')), t, t, tb_token, pvid)
            headers = {
                'method': 'GET',
                'authority': 'pub.alimama.com',
                'scheme': 'https',
                'path': '/items/search.json?%s' % url.split('search.json?')[-1],
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'x-requested-with': 'XMLHttpRequest',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
                'referer': 'https://pub.alimama.com',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.5',
            }
            res = self.get_url(url, headers)
            print(res.text)
            rj = res.json()
            if rj['data']['pageList'] != None:
                insert_sql = "INSERT INTO taojin_query_record(wx_bot, good_title, good_price, good_coupon, username, create_time) VALUES('" + bot_info['NickName'] + "', '" + rj['data']['pageList'][0]['title'] + "', '" + str(rj['data']['pageList'][0]['zkPrice']) + "', '"+ str(rj['data']['pageList'][0]['couponAmount']) +"', '" + userInfo['NickName'] + "', '" + str(time.time()) + "')"
                cm.ExecNonQuery(insert_sql)
                cm.Close()
                return rj['data']['pageList'][0]
            else:
                return 'no match item'
        except Exception as e:
            trace = traceback.format_exc()
            self.logger.warning("error:{},trace:{}".format(str(e), trace))

    # 获取商品详情
    def get_group_detail(self, q, msg):
        cm = ConnectMysql()

        chatrooms = itchat.search_chatrooms(userName=msg['FromUserName'])

        try:
            t = int(time.time() * 1000)
            tb_token = self.se.cookies.get('_tb_token_', domain="pub.alimama.com")
            pvid = '10_%s_1686_%s' % (self.myip, t)
            url = 'http://pub.alimama.com/items/search.json?q=%s&_t=%s&auctionTag=&perPageSize=40&shopTag=&t=%s&_tb_token_=%s&pvid=%s' % (
                urllib.quote(q.encode('utf8')), t, t, tb_token, pvid)
            headers = {
                'method': 'GET',
                'authority': 'pub.alimama.com',
                'scheme': 'https',
                'path': '/items/search.json?%s' % url.split('search.json?')[-1],
                'accept': 'application/json, text/javascript, */*; q=0.01',
                'x-requested-with': 'XMLHttpRequest',
                'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
                'referer': 'https://pub.alimama.com',
                'accept-encoding': 'gzip, deflate, br',
                'accept-language': 'en-US,en;q=0.5',
            }
            res = self.get_url(url, headers)
            print(res.text)
            rj = res.json()
            if rj['data']['pageList'] != None:
                insert_sql = "INSERT INTO taojin_query_record(wx_bot, good_title, good_price, good_coupon, username, create_time) VALUES('" + bot_info['NickName'] + "', '" + rj['data']['pageList'][0]['title'] + "', '" + str(rj['data']['pageList'][0]['zkPrice']) + "', '"+ str(rj['data']['pageList'][0]['couponAmount']) +"', '" + chatrooms['NickName'] + "', '" + str(time.time()) + "')"
                cm.ExecNonQuery(insert_sql)
                cm.Close()
                return rj['data']['pageList'][0]
            else:
                return 'no match item'
        except Exception as e:
            trace = traceback.format_exc()
            self.logger.warning("error:{},trace:{}".format(str(e), trace))

    # 获取淘宝客链接
    def get_tk_link(self, auctionid):
        t = int(time.time() * 1000)
        tb_token = self.se.cookies.get('_tb_token_', domain="pub.alimama.com")
        pvid = '10_%s_1686_%s' % (self.myip, t)
        try:
            gcid, siteid, adzoneid = self.__get_tk_link_s1(auctionid, tb_token, pvid)
            self.__get_tk_link_s2(gcid, siteid, adzoneid, auctionid, tb_token, pvid)
            res = self.__get_tk_link_s3(auctionid, adzoneid, siteid, tb_token, pvid)
            return res
        except Exception as e:
            trace = traceback.format_exc()
            self.logger.warning("error:{},trace:{}".format(str(e), trace))

    # 第一步，获取推广位相关信息
    def __get_tk_link_s1(self, auctionid, tb_token, pvid):
        url = 'http://pub.alimama.com/common/adzone/newSelfAdzone2.json?tag=29&itemId=%s&blockId=&t=%s&_tb_token_=%s&pvid=%s' % (
            auctionid, int(time.time() * 1000), tb_token, pvid)
        headers = {
            'Host': 'pub.alimama.com',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            'Referer': 'http://pub.alimama.com/promo/search/index.htm',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2',
        }
        res = self.get_url(url, headers)
        # self.logger.debug(res.text)
        rj = res.json()
        gcid = rj['data']['otherList'][0]['gcid']
        siteid = rj['data']['otherList'][0]['siteid']
        adzoneid = rj['data']['otherAdzones'][0]['sub'][0]['id']
        return gcid, siteid, adzoneid

    # post数据
    def __get_tk_link_s2(self, gcid, siteid, adzoneid, auctionid, tb_token, pvid):
        url = 'http://pub.alimama.com/common/adzone/selfAdzoneCreate.json'
        data = {
            'tag': '29',
            'gcid': gcid,
            'siteid': siteid,
            'selectact': 'sel',
            'adzoneid': adzoneid,
            't': int(time.time() * 1000),
            '_tb_token_': tb_token,
            'pvid': pvid,
        }
        headers = {
            'Host': 'pub.alimama.com',
            'Content-Length': str(len(json.dumps(data))),
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Origin': 'http://pub.alimama.com',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Referer': 'http://pub.alimama.com/promo/search/index.htm',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2',
        }

        res = self.post_url(url, headers, data)
        return res

    # 获取口令
    def __get_tk_link_s3(self, auctionid, adzoneid, siteid, tb_token, pvid):
        url = 'http://pub.alimama.com/common/code/getAuctionCode.json?auctionid=%s&adzoneid=%s&siteid=%s&scenes=1&t=%s&_tb_token_=%s&pvid=%s' % (
            auctionid, adzoneid, siteid, int(time.time() * 1000), tb_token, pvid)
        headers = {
            'Host': 'pub.alimama.com',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'X-Requested-With': 'XMLHttpRequest',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            'Referer': 'http://pub.alimama.com/promo/search/index.htm',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2',
        }
        res = self.get_url(url, headers)
        rj = json.loads(res.text)
        return rj['data']

    def get_real_url(self, url):
        # return "https://detail.tmall.com/item.htm?id=548726815314"
        try:
            headers = {
                'Host': url.split('http://')[-1].split('/')[0],
                'Upgrade-Insecure-Requests': '1',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                'Accept-Encoding': 'gzip, deflate, sdch',
                'Accept-Language': 'zh,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2',
            }
            res = self.get_url(url, headers)
            if re.search(r'itemId\":\d+', res.text):
                item_id = re.search(r'itemId\":\d+', res.text).group().replace('itemId":', '').replace('https://',
                                                                                                       'http://')
                r_url = "https://detail.tmall.com/item.htm?id=%s" % item_id
            elif re.search(r"var url = '.*';", res.text):
                r_url = re.search(r"var url = '.*';", res.text).group().replace("var url = '", "").replace("';",
                                                                                                           "").replace(
                    'https://', 'http://')
            else:
                r_url = res.url
            if 's.click.taobao.com' in r_url:
                r_url = self.handle_click_type_url(r_url)
            else:
                while ('detail.tmall.com' not in r_url) and ('item.taobao.com' not in r_url) and (
                            'detail.m.tmall.com' not in r_url):
                    headers1 = {
                        'Host': r_url.split('http://')[-1].split('/')[0],
                        'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Encoding': 'gzip, deflate, sdch',
                        'Accept-Language': 'zh,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2',
                    }
                    res2 = self.get_url(r_url, headers1)
                    self.logger.debug("{},{},{},{}".format(res2.url, res2.status_code, res2.history, res2.text))
                    r_url = res2.url

            # self.logger.debug(r_url)
            return r_url
        except Exception as e:
            self.logger.warning(str(e))
            return url

    def handle_click_type_url(self, url):
        # step 1
        headers = {
            'method': 'GET',
            'authority': 's.click.taobao.com',
            'scheme': 'https',
            'path': '/t?%s' % url.split('/t?')[-1],
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2',
        }
        res = self.get_url(url, headers)
        self.logger.debug("{},{},{}".format(res.url, res.status_code, res.history))
        url2 = res.url

        # step 2
        headers2 = {
            'referer': url,
            'method': 'GET',
            'authority': 's.click.taobao.com',
            'scheme': 'https',
            'path': '/t?%s' % url2.split('/t?')[-1],
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2',
        }
        res2 = self.get_url(url2, headers2)
        self.logger.debug("{},{},{}".format(res2.url, res2.status_code, res2.history))
        url3 = urllib.unquote(res2.url.split('t_js?tu=')[-1])

        # step 3
        headers3 = {
            'referer': url2,
            'method': 'GET',
            'authority': 's.click.taobao.com',
            'scheme': 'https',
            'path': '/t?%s' % url3.split('/t?')[-1],
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh,en-US;q=0.8,en;q=0.6,zh-CN;q=0.4,zh-TW;q=0.2',
        }
        res3 = self.get_url(url3, headers3)
        self.logger.debug("{},{},{}".format(res3.url, res3.status_code, res3.history))
        r_url = res3.url

        return r_url

    def get_order(self, msg, times, orderId, userInfo):

        timestr = re.sub('-', '', times)
        order_id = int(orderId)

        cm = ConnectMysql()

        bot_info = itchat.search_friends(userName=msg['ToUserName'])

        # 查询用户是否有上线
        check_order_sql = "SELECT * FROM taojin_order WHERE order_id='" + str(order_id) + "' AND wx_bot = '" +bot_info['NickName']+ "';"
        check_order_res = cm.ExecQuery(check_order_sql)

        # 判断该订单是否已经提现
        if len(check_order_res) >= 1:
            cm.Close()
            send_text ='''
一一一一 订单消息 一一一一

订单【%s】已经成功返利，请勿重复提交订单信息！
回复【个人信息】 查看订单及返利信息
如有疑问！请联系管理员
            ''' % (msg['Text'])
            return {"info":"order_exit","send_text":send_text}

        endTime = time.strftime('%Y-%m-%d', time.localtime(time.time()))

        startTime = str((datetime.date.today() - relativedelta(months=+1)))

        t = str(round(time.time()))

        try:
            url = "http://pub.alimama.com/report/getTbkPaymentDetails.json?startTime="+startTime+"&endTime="+endTime+"&payStatus=3&queryType=1&toPage=1&perPageSize=50&total=&t="+t+"&pvid=&_tb_token_=f8b388e3f3e37&_input_charset=utf-8"

            headers = {
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "Accept-Encoding": "gzip, deflate",
                "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                "Cache-Control": "no-cache",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "Host": "pub.alimama.com",
                "Pragma": "no-cache",
                "Referer": "http://pub.alimama.com/myunion.htm?spm=a219t.7900221/1.a214tr8.2.3d7c75a560ieiE",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:59.0) Gecko/20100101 Firefox/59.0",
                "X-Requested-With": "XMLHttpRequest"
            }

            res = self.get_url(url, headers)

            res_dict = json.loads(res.text)
            print(res_dict, url)

            for item in res_dict['data']['paymentList']:
                if int(order_id) == int(item['taobaoTradeParentId']):
                    res = self.changeInfo(msg, item, order_id, userInfo)
                    return res

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

            return {'info': 'not_order', 'user_text': user_text}
        except Exception as e:
            self.logger.debug(e)
            return {"info":"feild"}


    def changeInfo(self, msg, info, order_id, userInfo):
        print('info dddddddd')
        try:
            cm = ConnectMysql()

            bot_info = itchat.search_friends(userName=msg['ToUserName'])

            # 查询用户是否有上线
            check_user_sql = "SELECT * FROM taojin_user_info WHERE wx_number='" + str(userInfo['NickName']) + "' AND wx_bot='"+ bot_info['NickName'] +"';"
            check_user_res = cm.ExecQuery(check_user_sql)

            # 判断是否已经有个人账户，没有返回信息
            if len(check_user_res) < 1:
                cm.Close()
                return {"info":"not_info"}
            else:

                get_query_sql = "SELECT * FROM taojin_query_record WHERE good_title='" + info['auctionTitle'] + "'AND username='" + check_user_res[0][2] + "' AND wx_bot='"+ bot_info['NickName'] +"' ORDER BY create_time LIMIT 1;"

                get_query_info = cm.ExecQuery(get_query_sql)

                # 定义SQL语句 查询用户是否已经存在邀请人
                # 判断是否已经有邀请人了
                if check_user_res and check_user_res[0][17] != '0':

                    get_parent_sql = "SELECT * FROM taojin_user_info WHERE lnivt_code='" + str(check_user_res[0][17]) + "' AND wx_bot='"+ bot_info['NickName'] +"';"

                    get_parent_info = cm.ExecQuery(get_parent_sql)

                    add_balance = round(float(info['feeString']) * 0.3, 2)
                    withdrawals_amount = round(float(check_user_res[0][9]) + add_balance, 2)
                    taobao_rebate_amount = round(float(check_user_res[0][8]) + add_balance, 2)
                    total_rebate_amount = round(float(check_user_res[0][6]) + add_balance, 2)
                    save_money = round(check_user_res[0][10] + (float(get_query_info[0][3]) - float(info['realPayFeeString'])) + add_balance, 2)
                    total_order_num = int(check_user_res[0][11]) + 1
                    taobao_order_num = int(check_user_res[0][13]) + 1

                    add_parent_balance = round(float(info['feeString']) * 0.1, 2)
                    friends_rebatr = float(get_parent_info[0][19]) + float(add_balance)
                    withdrawals_amount2 = round(float(get_parent_info[0][9]) + float(add_balance) * 0.1, 2)

                    cm.ExecNonQuery("UPDATE taojin_user_info SET withdrawals_amount='" + str(withdrawals_amount) + "', save_money='"+ str(save_money) +"', taobao_rebate_amount='"+ str(taobao_rebate_amount) +"', total_rebate_amount='"+ str(total_rebate_amount) +"', order_quantity='"+str(total_order_num)+"', taobao_order_quantity='"+str(taobao_order_num)+"', update_time='"+str(time.time())+"' WHERE wx_number='" + str(userInfo['NickName']) + "' AND wx_bot='"+ bot_info['NickName'] +"';")
                    cm.ExecNonQuery("UPDATE taojin_user_info SET withdrawals_amount='" + str(withdrawals_amount2) + "', friends_rebate='"+str(friends_rebatr)+"', update_time='"+str(time.time())+"' WHERE lnivt_code='" + str(check_user_res[0][17]) + "' AND wx_bot='"+ bot_info['NickName'] +"';")

                    cm.ExecNonQuery("INSERT INTO taojin_order(wx_bot, username, order_id, order_source) VALUES('"+ bot_info['NickName'] +"', '"+str(userInfo['NickName'])+"', '"+str(order_id)+"', '2')")

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
                    ''' % (check_user_res[0][4], add_parent_balance)

                    user_text = '''
    一一一一系统消息一一一一

    订单【%s】已完成！
    返利金%s元已发放到您的个人账户！

    回复【提现】可申请账户余额提现
    回复【个人信息】可看个当前账户信息

    分享【京东商品链接】或者【淘口令】精准查询商品优惠券和返利信息！
    分享【VIP视频链接】免费查看高清VIP视频！

    优惠券使用教程：
    http://t.cn/RnAKqWW
    京东优惠券网站：
    http://jdyhq.ptjob.net
    淘宝优惠券网站：
    http://tbyhq.ptjob.net
    邀请好友得返利：
    http://t.cn/RnAKafe
                    ''' % (order_id, add_balance)
                    cm.Close()
                    return {'parent_user_text': parent_user_text, 'user_text': user_text, 'info': 'success', 'parent': get_parent_info[0][1]}
                else:
                    print('aabbacc')
                    add_balance = round(float(info['feeString']) * 0.3, 2)
                    withdrawals_amount = round(float(check_user_res[0][9]) + add_balance, 2)
                    taobao_rebate_amount = round(float(check_user_res[0][8]) + add_balance, 2)
                    total_rebate_amount = round(float(check_user_res[0][6]) + add_balance, 2)
                    save_money = round(check_user_res[0][10] + (float(get_query_info[0][3]) - float(info['realPayFeeString'])) + add_balance, 2)
                    total_order_num = int(check_user_res[0][11]) + 1
                    taobao_order_num = int(check_user_res[0][13]) + 1

                    cm.ExecNonQuery("UPDATE taojin_user_info SET withdrawals_amount='" + str(
                        withdrawals_amount) + "', save_money='" + str(save_money) + "', taobao_rebate_amount='" + str(
                        taobao_rebate_amount) + "', total_rebate_amount='" + str(
                        total_rebate_amount) + "', order_quantity='"+str(total_order_num)+"', taobao_order_quantity='"+str(taobao_order_num)+"', update_time='" + str(time.time()) + "' WHERE wx_number='" + str(
                        userInfo['NickName']) + "' AND wx_bot='"+ bot_info['NickName'] +"';")


                    sssq = "INSERT INTO taojin_order(wx_bot, username, order_id, order_source) VALUES('" + str(bot_info['NickName']) + "', '"+str(userInfo['NickName'])+"', '"+str(order_id)+"', 2)"
                    print(sssq)
                    cm.ExecNonQuery(sssq)

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
    一一一一系统消息一一一一

    订单【%s】已完成！
    返利金%s元已发放到您的个人账户！

    回复【提现】可申请账户余额提现
    回复【个人信息】可看个当前账户信息

    分享【京东商品链接】或者【淘口令】精准查询商品优惠券和返利信息！
    分享【VIP视频链接】免费查看高清VIP视频！

    优惠券使用教程：
    http://t.cn/RnAKqWW
    京东优惠券网站：
    http://jdyhq.ptjob.net
    淘宝优惠券网站：
    http://tbyhq.ptjob.net
    邀请好友得返利：
    http://t.cn/RnAKafe
                                ''' % (order_id, add_balance)
                    cm.Close()
                    return {'user_text': user_text, 'info': 'not_parent_and_success'}
        except Exception as e:
            self.logger.debug(e)
            return {'info': 'feild'}


if __name__ == '__main__':
    al = Alimama()
    # al.login()
    # q = u'现货 RS版 树莓派3代B型 Raspberry Pi 3B 板载wifi和蓝牙'
    # q = u'蔻斯汀玫瑰身体护理套装沐浴露身体乳爽肤水滋润全身保湿补水正品'
    # q = u'DIY个性定制T恤 定做工作服短袖 男女夏季纯棉广告文化衫Polo印制'
    q = u'防晒衣女2017女装夏装新款印花沙滩防晒服薄中长款大码白色短外套'
    # res = al.get_detail(q)
    # auctionid = res['auctionId']
    # al.get_tk_link(auctionid)
    # url = 'http://c.b1wt.com/h.SQwr1X?cv=kzU8ZvbiEa8&sm=796feb'
    # al.get_real_url(url)
    # url = 'http://c.b1wt.com/h.S9fQZb?cv=zcNtZvbH4ak&sm=79e4be'
    # al.get_real_url(url)
    # url = 'http://c.b1wt.com/h.S9gdyy?cv=RW5EZvbuYBw&sm=231894'
    # al.get_real_url(url)
    # url = 'http://c.b1wt.com/h.S8ppn7?cv=ObUrZvZ3oH9&sm=1b02f8'
    # al.get_real_url(url)
    # url = 'http://c.b1wt.com/h.SQ70kv?cv=L5HpZv0w4hJ'
    # url = 'http://c.b1wt.com/h.S9A0pK?cv=8grnZvYkU14&sm=efb5b7'
    url = 'http://zmnxbc.com/s/nlO3j?tm=95b078'
    al.get_real_url(url)
