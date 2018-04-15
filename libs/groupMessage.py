# -*-coding: UTF-8-*-
import time
import webbrowser
from flask import Flask
from flask import request
import configparser
from libs.mysql import ConnectMysql
from libs import wx_bot
from threading import Thread
from bottle import template
from libs.wx_bot import *
from libs.mediaJd import MediaJd
from itchat.content import *
import datetime

app = Flask(__name__)
mjd = MediaJd()
config = configparser.ConfigParser()
config.read('config.conf',encoding="utf-8-sig")

class FormData(object):
	def run(self):
		run_app()

	def async(f):
		def wrapper(*args, **kwargs):
			thr = Thread(target=f, args=args, kwargs=kwargs)
			thr.start()

		return wrapper

	# 获取群
	@async
	def groupMessages(self):
		time.sleep(30)
		yorn = input("是否重新选群？y/n:")
		if yorn == 'n':
			self.start_send_msg_thread()
			return

		print('start.....')
		cm = ConnectMysql()

		res = itchat.web_init()

		select_sql = "DELETE FROM taojin_group_message WHERE username='" + str(res['User']['NickName']) + "';"
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

		self.run()

	# 群发消息
	def send_group_meg(self):
		cm = ConnectMysql()

		res = itchat.web_init()

		select_sql = "SELECT * FROM taojin_group_message WHERE username='" + str(res['User']['NickName']) + "';"

		group_info = cm.ExecQuery(select_sql)

		while True:

			a = datetime.datetime.now().hour

			if int(a) < 8 | int(a) >= 20:
				print('时间不够')
				continue

			print('ok')
			time.sleep(1200)

			data_sql = "SELECT * FROM taojin_good_info WHERE status=1 AND wx_bot='"+ res['User']['NickName'] +"' LIMIT 1"

			data1 = cm.ExecQuery(data_sql)
			if data1 == ():
				mjd.get_good_info(res['User']['NickName'])
				cm.Close()
			cm2 = ConnectMysql()
			data = cm2.ExecQuery(data_sql)
			text = '''
一一一一优惠信息一一一一

【商品名】%s
【京东价】%s元
【优惠券】%s元
【券后价】%s元
领券链接:%s

请点击链接领取优惠券，下单购买！
	                ''' % (data[0][3], data[0][5], data[0][7], data[0][8], data[0][10])

			delete_sql = "UPDATE taojin_good_info SET status='2' WHERE id='" + str(data[0][0]) + "'  AND wx_bot='"+ res['User']['NickName'] +"'"
			cm.ExecNonQuery(delete_sql)

			img_name = data[0][3].split('/')

			img_path = "images/" + img_name[-1]
			for item in group_info:
				time.sleep(30)
				itchat.send_image(img_path, item[2])
				itchat.send(text, item[2])

	# 启动一个线程，定时发送商品信息
	def start_send_msg_thread(self):
		t = Thread(target=self.send_group_meg, args=())
		t.setDaemon(True)
		t.start()


fmm = FormData()

@app.route('/', methods=['GET', 'POST'])
def index():
	return "<h1>访问form路由</h1>"


@app.route('/form', methods=['GET', 'POST'])
def formShow():
	# 使用浏览器打开html
	html = open('form.html', 'r', encoding='utf-8')
	return html.read()

@app.route('/formdata', methods=['POST'])
def setData():
	cm = ConnectMysql()
	# 需要从request对象读取表单内容：
	formdata = request.form
	username = formdata['username']
	for item in formdata:
		if item != 'username':
			insert_sql = "INSERT INTO taojin_group_message(username, groupid, groupname, create_time) VALUES('"+username+"', '"+item+"', '"+formdata[item]+"', '"+str(time.time())+"')"
			cm.ExecNonQuery(insert_sql)
	# 执行群发任务
	fmm.start_send_msg_thread()
	return "添加成功！"
def run_app():
	webbrowser.open('http:127.0.0.1:5000/form')
	app.run()