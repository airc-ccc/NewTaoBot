# -*-coding: UTF-8-*-
import time
import webbrowser
from flask import Flask
from flask import request
from libs.mysql import ConnectMysql
from libs import wx_bot

app = Flask(__name__)

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
	wx_bot.start_send_msg_thread()
	return "添加成功！"
def run_app():
	webbrowser.open('http:127.0.0.1:5000/form')
	app.run()

class FormData(object):
	def run(self):
		run_app()