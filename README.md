# wx_jd_fanli
微信 京东 返利

---
20180308 更新

python3

---

这个一个微信京东返利"机器人", 在京东里点击分享，分享给商品给机器人，机器人自动返回领券链接，下单链接。

功能上主要有两部分：
#### 京东
京东联盟接口申请资质太高，自己抓包分析实现了。：
```
1、登录京东联盟
2、根据sharing搜索相关的商品
3、返回领券下单链接
```

#### 依赖
```
requests
Selenium
BeautifulSoup
itchat

```

#### 使用
#####命令行运行, 获取Cookie,只限第一次，或者Cookie失效
```
python getCookies.py

```
##### 获取领券信息
```
python getData.py

```
