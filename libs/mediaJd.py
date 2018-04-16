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
from libs import utils
from bs4 import BeautifulSoup
from time import strftime,gmtime
from libs.mysql import ConnectMysql
from libs.wx_bot import *
from itchat.content import *
from bottle import template

logger = utils.init_logger()

cookie_fname = 'cookies_jd.txt'
sysstr = platform.system()
config = configparser.ConfigParser()
config.read('config.conf',encoding="utf-8-sig")

class MediaJd:
    def __init__(self):
        self.se = requests.session()
        self.load_cookies()

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
        dict_str['positionId'] = 1194027498
        dict_str['positionName'] = '京推推推广位'
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




