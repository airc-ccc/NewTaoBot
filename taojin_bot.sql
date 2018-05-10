/*
SQLyog 企业版 - MySQL GUI v8.14 
MySQL - 5.5.5-10.1.30-MariaDB : Database - taojin_bot
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`taojin_bot` /*!40100 DEFAULT CHARACTER SET latin1 */;

USE `taojin_bot`;

/*Table structure for table `taojin_current_log` */

DROP TABLE IF EXISTS `taojin_current_log`;

CREATE TABLE `taojin_current_log` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `wx_bot` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT 'å¾®ä¿¡æœºå™¨äºº',
  `username` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '0' COMMENT 'æçŽ°äºº',
  `amount` float(11,2) NOT NULL DEFAULT '1.00' COMMENT 'æçŽ°é‡‘é¢',
  `create_time` int(11) NOT NULL COMMENT 'æçŽ°æ—¶é—´',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1 CHECKSUM=1 DELAY_KEY_WRITE=1 ROW_FORMAT=DYNAMIC;

/*Data for the table `taojin_current_log` */

insert  into `taojin_current_log`(`id`,`wx_bot`,`username`,`amount`,`create_time`) values (1,'跑堂优惠券','追梦的蚂蚁',1.31,1523805351);

/*Table structure for table `taojin_good_info` */

DROP TABLE IF EXISTS `taojin_good_info`;

CREATE TABLE `taojin_good_info` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `wx_bot` varchar(255) CHARACTER SET utf8 NOT NULL,
  `skuid` bigint(20) NOT NULL COMMENT 'skuid',
  `title` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '商品title',
  `image` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '商品图片',
  `price` float NOT NULL COMMENT '商品原价',
  `rebate` float NOT NULL COMMENT '返利价格',
  `yhq_price` int(11) NOT NULL DEFAULT '0' COMMENT '优惠券价格',
  `coupon_price` float NOT NULL DEFAULT '0' COMMENT '券后价',
  `shoturl` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '商品购买链接',
  `shotcouponurl` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '0' COMMENT '优惠券链接',
  `status` tinyint(1) NOT NULL COMMENT '商品状态，1 未发送，2 已发送',
  `create_time` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=latin1 CHECKSUM=1 DELAY_KEY_WRITE=1 ROW_FORMAT=DYNAMIC;

/*Data for the table `taojin_good_info` */

insert  into `taojin_good_info`(`id`,`wx_bot`,`skuid`,`title`,`image`,`price`,`rebate`,`yhq_price`,`coupon_price`,`shoturl`,`shotcouponurl`,`status`,`create_time`) values (1,'跑堂优惠券',24152462007,'运动套装男士春秋新款运动服套装男长袖休闲套装男开衫跑步健身服 H9001【黑款】 XL/175','http://img14.360buyimg.com/n1/jfs/t17779/281/1449075664/29840/c1ab6b57/5aca2db0N3bdc0249.jpg',168,0.71,50,118,'https://union-click.jd.com/jdc?d=gqPLgr','https://union-click.jd.com/jdc?d=Seh1p6',2,1523896702),(2,'跑堂优惠券',1030053488,'航睿 大众新朗逸朗行宝来速腾迈腾捷达桑塔纳途观斯柯达明锐车载导航倒车影像后视一体车机 4G版(北斗+GPS)+高清后视+记录仪(包安装)','http://img14.360buyimg.com/n1/jfs/t12637/230/2663582491/429064/8fc2477b/5ac36284Nad9a54ce.jpg',1299,29.98,50,1249,'https://union-click.jd.com/jdc?d=oNCQhv','https://union-click.jd.com/jdc?d=GVKAVX',2,1523896703),(3,'跑堂优惠券',1512698159,'苏泊尔（SUPOR） 304不锈钢蒸锅28cm双层复底汤锅二层蒸笼电磁炉锅具SZ28B5','http://img14.360buyimg.com/n1/jfs/t17680/133/1664285479/400680/d6388f9/5ad46fbeN50938604.jpg',159,4.17,20,139,'https://union-click.jd.com/jdc?d=iH3Aqv','https://union-click.jd.com/jdc?d=Uk9esm',2,1523896704),(4,'跑堂优惠券',11324658381,'盾郎（donow） 迷彩服男套装军绿套装作训服户外军迷服饰耐磨工装猎人劳保工作服 猎人套装 170','http://img14.360buyimg.com/n1/jfs/t8815/332/239174798/328906/237dee66/59a3f7acN85a001a5.jpg',98,4.68,20,78,'https://union-click.jd.com/jdc?d=d2GijK','https://union-click.jd.com/jdc?d=dLnRqu',2,1523896705),(5,'跑堂优惠券',11324658378,'盾郎（donow） 迷彩服男套装军绿套装作训服户外军迷服饰耐磨工装猎人劳保工作服 猎人套装 180','http://img14.360buyimg.com/n1/jfs/t8815/332/239174798/328906/237dee66/59a3f7acN85a001a5.jpg',98,4.68,20,78,'https://union-click.jd.com/jdc?d=zx9Oyr','https://union-click.jd.com/jdc?d=YncDc8',2,1523896706),(6,'跑堂优惠券',11324658380,'盾郎（donow） 迷彩服男套装军绿套装作训服户外军迷服饰耐磨工装猎人劳保工作服 猎人套装 175','http://img14.360buyimg.com/n1/jfs/t8815/332/239174798/328906/237dee66/59a3f7acN85a001a5.jpg',98,4.68,20,78,'https://union-click.jd.com/jdc?d=o0Qygt','https://union-click.jd.com/jdc?d=NG48UA',2,1523896707),(7,'跑堂优惠券',25412457653,'Caesar/凯撒大帝新款商务真皮正装皮鞋男英伦休闲鞋子男韩版男鞋 简约黑色 41','http://img14.360buyimg.com/n1/jfs/t15223/32/2128520745/82879/3aba3f61/5a6fd505N37d12b5b.jpg',389,17.94,90,299,'https://union-click.jd.com/jdc?d=ZvPLA1','https://union-click.jd.com/jdc?d=xAnxH1',2,1523896707),(8,'跑堂优惠券',10292153376,'沃隆 每日坚果礼盒 混合坚果零食什锦果仁 A款=25g*30袋','http://img14.360buyimg.com/n1/jfs/t15502/265/2427262655/352973/a1955676/5aa8f53bNa8d90bb1.jpg',149,6.25,10,139,'https://union-click.jd.com/jdc?d=Xx6jim','https://union-click.jd.com/jdc?d=SYpxvJ',2,1523896708),(9,'跑堂优惠券',11315763031,'美国爱康划船机41016家用静音可折叠健身运动器材风阻划船器 京东官方配送','http://img14.360buyimg.com/n1/jfs/t19120/184/1736902392/375817/2dcc3fe0/5ad4045aN7170de26.jpg',3699,64.78,100,3599,'https://union-click.jd.com/jdc?d=zF2JXv','https://union-click.jd.com/jdc?d=7oAJ4j',2,1523896709),(10,'跑堂优惠券',11324658376,'盾郎（donow） 迷彩服男套装军绿套装作训服户外军迷服饰耐磨工装猎人劳保工作服 猎人套装 165','http://img14.360buyimg.com/n1/jfs/t8815/332/239174798/328906/237dee66/59a3f7acN85a001a5.jpg',98,4.68,20,78,'https://union-click.jd.com/jdc?d=XwqIaz','https://union-click.jd.com/jdc?d=95drq4',2,1523896711),(11,'跑堂优惠券',10974423049,'宝丽（EVERTOP） 电动沐浴刷搓背神器搓澡机洗澡按摩长柄智能自动去角质FD-ESS 蓝色','http://img14.360buyimg.com/n1/jfs/t14203/99/1900541843/305186/fa469a77/5a605ab3N1564c083.jpg',156,9.2,10,146,'https://union-click.jd.com/jdc?d=JqMaEI','https://union-click.jd.com/jdc?d=crvgnH',2,1523896713),(12,'跑堂优惠券',11324658375,'盾郎（donow） 迷彩服男套装军绿套装作训服户外军迷服饰耐磨工装猎人劳保工作服 猎人套装 185','http://img14.360buyimg.com/n1/jfs/t8815/332/239174798/328906/237dee66/59a3f7acN85a001a5.jpg',98,4.68,20,78,'https://union-click.jd.com/jdc?d=7mMVtV','https://union-click.jd.com/jdc?d=zSxHfn',2,1523896714),(13,'跑堂优惠券',11324658379,'盾郎（donow） 迷彩服男套装军绿套装作训服户外军迷服饰耐磨工装猎人劳保工作服 猎人套装 190','http://img14.360buyimg.com/n1/jfs/t8815/332/239174798/328906/237dee66/59a3f7acN85a001a5.jpg',98,4.68,20,78,'https://union-click.jd.com/jdc?d=lLoNsR','https://union-click.jd.com/jdc?d=6TuOkE',2,1523896714),(14,'跑堂优惠券',1470224983,'苏泊尔（SUPOR） 304不锈钢高压锅20cm复底压力锅4.0L电磁炉锅具YS20ED','http://img14.360buyimg.com/n1/jfs/t19243/166/1668335545/286600/931b533f/5ad4704eNd18c2253.jpg',199,8.05,20,179,'https://union-click.jd.com/jdc?d=kXoG5n','https://union-click.jd.com/jdc?d=cocBs8',2,1523896716),(15,'跑堂优惠券',15549169393,'雷德蒙 男士太阳镜男款墨镜女偏光镜潮人开车驾驶镜复古蛤蟆镜男款太阳眼镜 银色框 水银偏光片(送夜视镜)(再送墨镜)','http://img14.360buyimg.com/n1/jfs/t7903/159/1513306656/77164/25841b42/599d7660N93626ba7.jpg',59,1.62,5,54,'https://union-click.jd.com/jdc?d=Lhglfn','https://union-click.jd.com/jdc?d=PpMqHv',2,1523896718),(16,'跑堂优惠券',10387133981,'蓝眼兔女童凉鞋2018新品夏季真皮儿童露趾公主鞋中大童鱼嘴高跟鞋韩版女童鞋 粉色 36码/内长23.4(适合脚长22.9cm)','http://img14.360buyimg.com/n1/jfs/t19168/341/1243775928/567746/4a38e2cb/5ac2fe69N6a9d07be.jpg',99,1.19,20,79,'https://union-click.jd.com/jdc?d=QvlpE3','https://union-click.jd.com/jdc?d=twGs6Z',2,1523896719),(17,'跑堂优惠券',25052495736,'华晗无限魔方美国infinity cube解压神器无线方块益智玩具创意减压魔方骰子抖音同款 银色-升级版无限魔方','http://img14.360buyimg.com/n1/jfs/t16171/264/2539579905/113705/8e88d16e/5abb803dN34788df3.jpg',85,3.6,5,80,'https://union-click.jd.com/jdc?d=gVdR75','https://union-click.jd.com/jdc?d=fxlM5q',2,1523896719),(18,'跑堂优惠券',10109301357,'泓砚（HONGYAN） 客厅装饰画字画走廊玄关挂画手绘斗方葫芦画餐厅卧室壁画中堂画 斗方葫芦五福临门 三尺斗方（实木外框+有机玻璃）65*65cm/幅','http://img14.360buyimg.com/n1/jfs/t18211/260/964257199/412346/f099ed01/5ab1bca5N4cb28611.jpg',368,10.44,20,348,'https://union-click.jd.com/jdc?d=KJzrug','https://union-click.jd.com/jdc?d=zUI6ub',2,1523896721),(19,'跑堂优惠券',1016417538,'皇家猫粮 I27室内成猫粮2kg','http://img14.360buyimg.com/n1/jfs/t3058/359/2495961219/265971/b7c3c623/57e23d7fNf89b3559.jpg',127,3.21,20,107,'https://union-click.jd.com/jdc?d=K8eQQq','https://union-click.jd.com/jdc?d=LY6Nrm',2,1523896721),(20,'跑堂优惠券',25847557443,'汝铭童装男女童套装夏装纯棉韩版中小儿童宝宝两件套 子青-滑板河马 75码/110-120cm','http://img14.360buyimg.com/n1/jfs/t17596/316/1684293312/209638/7f1b78f9/5ad214a6Nc648ab56.jpg',59,2.25,34,25,'https://union-click.jd.com/jdc?d=l3XWlC','https://union-click.jd.com/jdc?d=0BS87Z',2,1523896722),(21,'跑堂优惠券',15865010148,'非针孔wifi微型智能摄像头网络监控隐形手机远程夜视版升级1080P 高清超小迷你家用摄像头 1080P升级版配16G','http://img14.360buyimg.com/n1/jfs/t7780/25/1845144621/119207/f38bc8fc/59a29961N00e3cc78.jpg',321.3,14.23,5,316.3,'https://union-click.jd.com/jdc?d=RtniwW','https://union-click.jd.com/jdc?d=eCKaiE',1,1523896723),(22,'跑堂优惠券',13035188048,'明星同款 vvc正品夏季遮阳帽子女夏天防紫外线防晒沙滩帽可折叠户外骑车太阳帽女神帽儿童帽 儿童款-粉色','http://img14.360buyimg.com/n1/jfs/t6883/7/1107263304/373017/a47e1ddf/597d407aN916ef43d.jpg',198,8.88,50,148,'https://union-click.jd.com/jdc?d=R5R0kY','https://union-click.jd.com/jdc?d=4n0H2r',1,1523896724),(23,'跑堂优惠券',15549169390,'雷德蒙 男士太阳镜男款墨镜女偏光镜潮人开车驾驶镜复古蛤蟆镜男款太阳眼镜 银色框 冰蓝偏光片(送夜视镜)(再送墨镜)','http://img14.360buyimg.com/n1/jfs/t7780/147/1511356745/92537/591a0c14/599d7471N0a1d2221.jpg',59,1.62,5,54,'https://union-click.jd.com/jdc?d=VYChMJ','https://union-click.jd.com/jdc?d=5Z0ApA',1,1523896725),(24,'跑堂优惠券',10573338457,'361° 童鞋 男童中大儿童运动鞋2018春秋新品透气网面跑步鞋小童休闲鞋夏季男童鞋 降落伞/芒果黄（大网孔） 38','http://img14.360buyimg.com/n1/jfs/t16777/304/1663565572/466568/f500ce78/5ad2fc0cN866f7c54.jpg',119,1.64,10,109,'https://union-click.jd.com/jdc?d=txCmmg','https://union-click.jd.com/jdc?d=7f6EPq',1,1523896726),(25,'跑堂优惠券',11125772349,'山特UPS（SANTAK） 山特UPS不间断电源C1K在线式内置电池 后备时间约25分钟 【京东仓库配送】山特C1K正品UPS','http://img14.360buyimg.com/n1/jfs/t3268/13/5749702450/140822/99a62f8f/58856039N3bc30c9b.jpg',1558,17.8,75,1483,'https://union-click.jd.com/jdc?d=MMJXTh','https://union-click.jd.com/jdc?d=fl05Gn',1,1523896727),(26,'跑堂优惠券',11324658377,'盾郎（donow） 迷彩服男套装军绿套装作训服户外军迷服饰耐磨工装猎人劳保工作服 猎人套装 160','http://img14.360buyimg.com/n1/jfs/t8815/332/239174798/328906/237dee66/59a3f7acN85a001a5.jpg',98,4.68,20,78,'https://union-click.jd.com/jdc?d=g4LWc6','https://union-click.jd.com/jdc?d=9UCJsK',1,1523896728),(27,'跑堂优惠券',10740931377,'六胜肽抗皱紧致玻尿酸原液男女面部精华液 六胜肽原液','http://img14.360buyimg.com/n1/jfs/t3241/105/3174844910/132979/783f1e5c/57ec938fNd7c055ae.jpg',68,2.61,10,58,'https://union-click.jd.com/jdc?d=snM8nL','https://union-click.jd.com/jdc?d=yMtp6g',1,1523896730),(28,'跑堂优惠券',1030053609,'航睿 大众新朗逸朗行宝来速腾迈腾捷达桑塔纳途观斯柯达明锐车载导航倒车影像后视一体车机 4G版(北斗+GPS)+高清后视(免费安装)','http://img14.360buyimg.com/n1/jfs/t12637/230/2663582491/429064/8fc2477b/5ac36284Nad9a54ce.jpg',1199,27.58,50,1149,'https://union-click.jd.com/jdc?d=sbo9Yv','https://union-click.jd.com/jdc?d=9bq6VN',1,1523896731),(29,'跑堂优惠券',15801862946,'【3件8折】正宗德州扒鸡500g/袋 五香脱骨扒鸡 山东特产 熟食烧鸡 厂家自营旗舰店','http://img14.360buyimg.com/n1/jfs/t17263/177/1152683462/161453/4c90cbc0/5abe61eaNc7c39192.png',29.9,1.67,2,27.9,'https://union-click.jd.com/jdc?d=ThKR6m','https://union-click.jd.com/jdc?d=dRoBFp',1,1523896732),(30,'跑堂优惠券',12550482193,'苏泊尔（SUPOR） 平底锅星星石系列麦饭石色不粘平底煎锅无油烟煎盘牛排烙饼锅燃气灶锅具 PJ28W5 28厘米 明火燃气灶专用','http://img14.360buyimg.com/n1/jfs/t18676/292/1685933514/370090/f2dda682/5ad46f54Ne2c72af1.jpg',169,4.47,20,149,'https://union-click.jd.com/jdc?d=IBTxaY','https://union-click.jd.com/jdc?d=z4ekGb',1,1523896733),(31,'跑堂优惠券',10292153378,'沃隆 每日坚果礼盒 混合坚果零食什锦果仁 混合款=A款15袋+B款15袋','http://img14.360buyimg.com/n1/jfs/t19633/200/815987278/341686/12924646/5aa9da46N124e9eb3.jpg',149,6.25,10,139,'https://union-click.jd.com/jdc?d=cb6NX1','https://union-click.jd.com/jdc?d=cgiriA',1,1523896734),(32,'跑堂优惠券',1525367342,'苏泊尔（SUPOR） 炒锅不粘锅34cm易清洁少油烟不生锈炒菜锅明火燃气锅具PC34S3','http://img14.360buyimg.com/n1/jfs/t18211/240/1693210313/317977/2445afc9/5ad46ed4N70240292.jpg',179,4.77,20,159,'https://union-click.jd.com/jdc?d=3R9xoT','https://union-click.jd.com/jdc?d=aXZwsX',1,1523896735),(33,'跑堂优惠券',11409738603,'盾郎（donow） 07体能服套装军装男特种兵训练T恤夏季军迷服饰户外运动速干短袖短裤 体能套装 190','http://img14.360buyimg.com/n1/jfs/t15661/163/2621942021/452525/34c40b17/5ab86010N73cb55e7.jpg',72,4.02,5,67,'https://union-click.jd.com/jdc?d=Skwjpb','https://union-click.jd.com/jdc?d=P0tZPV',1,1523896736),(34,'跑堂优惠券',1030053611,'航睿 大众新朗逸朗行宝来速腾迈腾捷达桑塔纳途观斯柯达明锐车载导航倒车影像后视一体车机 WiFi版大屏+高清后视+记录仪(免费安装)','http://img14.360buyimg.com/n1/jfs/t12637/230/2663582491/429064/8fc2477b/5ac36284Nad9a54ce.jpg',1199,27.58,50,1149,'https://union-click.jd.com/jdc?d=NvjmoT','https://union-click.jd.com/jdc?d=7vMHvF',1,1523896738),(35,'跑堂优惠券',17167192494,'先科 车载充电器一拖二 3.6A车充汽车点烟器式双usb车用多功能手机快充一分二 太空银+三合一充电线','http://img14.360buyimg.com/n1/jfs/t18109/76/1164760459/280574/e86b9f13/5abdd43dN655d7306.jpg',49,2.34,10,39,'https://union-click.jd.com/jdc?d=4bRfrX','https://union-click.jd.com/jdc?d=a5ntHQ',1,1523896739),(36,'跑堂优惠券',13035188046,'明星同款 vvc正品夏季遮阳帽子女夏天防紫外线防晒沙滩帽可折叠户外骑车太阳帽女神帽儿童帽 儿童款-蓝色','http://img14.360buyimg.com/n1/jfs/t6997/246/1072515586/413856/dd4b62ec/597d3fd5Nd6c7957d.jpg',198,8.88,50,148,'https://union-click.jd.com/jdc?d=xzpO07','https://union-click.jd.com/jdc?d=pxMXH5',1,1523896740),(37,'跑堂优惠券',13108974729,'华牧鲜 加拿大安格斯原切牛排套餐800g 牛扒 进口牛肉 雪花牛排4袋','http://img14.360buyimg.com/n1/jfs/t15007/215/1828097433/300561/67340c90/5a5967a4N7e6090f2.jpg',199,8.94,50,149,'https://union-click.jd.com/jdc?d=dupBM4','https://union-click.jd.com/jdc?d=LZF2SB',1,1523896741),(38,'跑堂优惠券',18606893166,'冬己 升级版迷你欢乐抓娃娃机 抖音同款儿童玩具小型夹公仔娃娃机迷你投币游戏机女孩玩具','http://img14.360buyimg.com/n1/jfs/t7510/273/4130751607/303540/efbf4917/5acac0d8Nc8ff48a0.jpg',299,0.88,5,294,'https://union-click.jd.com/jdc?d=YZhAeh','https://union-click.jd.com/jdc?d=TnZSUX',1,1523896742),(39,'跑堂优惠券',26138805616,'妍叶堂牙斑净牙齿美白速效去黄牙烟牙垢黑渍洗牙粉液牙贴去除牙结石祛咖啡渍一擦净牙膏白牙素洁牙素日本牙笔','http://img14.360buyimg.com/n1/jfs/t18436/202/1483003086/292181/7db0041c/5acb004aNc3c3c2a0.jpg',29,1.14,10,19,'https://union-click.jd.com/jdc?d=Zdrbyd','https://union-click.jd.com/jdc?d=3SZtlx',1,1523896742),(40,'跑堂优惠券',25126605134,'华晗减压骰子减压玩具美国减压魔方 fidget cube无限魔方解压玩具发泄神器抵抗烦躁焦虑方块 铅灰色','http://img14.360buyimg.com/n1/jfs/t16300/147/2618347639/33964/bd8b0040/5abb7529Ne145e7b6.jpg',58,2.38,5,53,'https://union-click.jd.com/jdc?d=jgJdXp','https://union-click.jd.com/jdc?d=yGY81M',1,1523896744),(41,'跑堂优惠券',15683245441,'图拉斯  汽车香水摆件 车载香水出风口车内香膏车用香水夹座 汽车用品清新空气香薰棒 典雅黑【配送柠檬/橄榄/古龙/海洋味香薰芯】','http://img14.360buyimg.com/n1/jfs/t16180/107/2297906702/265011/89a5f053/5a9f6774N798cc64b.jpg',68,3.48,10,58,'https://union-click.jd.com/jdc?d=JsZ3hd','https://union-click.jd.com/jdc?d=WcufX9',1,1523896744),(42,'跑堂优惠券',20451574415,'微型无线监控摄像头智能网络高清夜视监控设备套装家用手机远程监控摄像头 wifi1080P 高配版','http://img14.360buyimg.com/n1/jfs/t11803/142/1585637358/130128/f3f58943/5a041765Nf1cc62d6.jpg',510,22.72,5,505,'https://union-click.jd.com/jdc?d=LdOsCt','https://union-click.jd.com/jdc?d=k8oTg4',1,1523896745),(43,'跑堂优惠券',1027092051,'航睿起亚安卓大屏K2K3K4K5狮跑智跑赛拉图瑞纳IX25车载导航倒车影像后视测速一体机 4G版(北斗+GPS)-K2K3K4K5+记录仪','http://img14.360buyimg.com/n1/jfs/t19762/235/1299170537/367280/99b6ebda/5ac36397Ne86d1109.jpg',1299,29.98,50,1249,'https://union-click.jd.com/jdc?d=Nx5a15','https://union-click.jd.com/jdc?d=4fCzsb',1,1523896746),(44,'跑堂优惠券',16049259636,'修正（XiuZheng） 血压计 家用全自动上臂式高精准电子血压测量仪 BSX565 双人记忆一台抵两台+语音播报+USB电池双重供电','http://img14.360buyimg.com/n1/jfs/t7606/195/2114425417/180506/ea6ab443/59a8be50Nd0f68953.jpg',168,1.47,5,163,'https://union-click.jd.com/jdc?d=VCm09q','https://union-click.jd.com/jdc?d=EdN9V7',1,1523896747),(45,'跑堂优惠券',25977046135,'古卡顿2018夏季新品休闲鞋春季男士韩版透气平底飞织运动鞋潮流板鞋新款学生平底网鞋男跑步鞋子 1801白色 42','http://img14.360buyimg.com/n1/jfs/t16630/341/1466621203/423681/48fb5079/5acb7677Na2245e6a.jpg',158,4.44,10,148,'https://union-click.jd.com/jdc?d=VW5v0l','https://union-click.jd.com/jdc?d=nZMI5o',1,1523896748),(46,'跑堂优惠券',11409738615,'盾郎（donow） 07体能服套装军装男特种兵训练T恤夏季军迷服饰户外运动速干短袖短裤 体能上衣 170','http://img14.360buyimg.com/n1/jfs/t15661/163/2621942021/452525/34c40b17/5ab86010N73cb55e7.jpg',45,2.4,5,40,'https://union-click.jd.com/jdc?d=3mnx6M','https://union-click.jd.com/jdc?d=empZL3',1,1523896749);

/*Table structure for table `taojin_group_message` */

DROP TABLE IF EXISTS `taojin_group_message`;

CREATE TABLE `taojin_group_message` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '机器人名称',
  `groupid` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '群id',
  `groupname` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '群名称',
  `create_time` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=latin1 CHECKSUM=1 DELAY_KEY_WRITE=1 ROW_FORMAT=DYNAMIC;

/*Data for the table `taojin_group_message` */

insert  into `taojin_group_message`(`id`,`username`,`groupid`,`groupname`,`create_time`) values (9,'跑堂优惠券','@@f6c5e22d451ea89e9a20ea7cbf737298962d6ddd4d5e57bbaa10811072cf66be','跑堂优惠券16',1523899532);

/*Table structure for table `taojin_order` */

DROP TABLE IF EXISTS `taojin_order`;

CREATE TABLE `taojin_order` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `wx_bot` varchar(255) CHARACTER SET utf8 NOT NULL,
  `username` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT 'ç”¨æˆ·å',
  `order_id` char(32) CHARACTER SET utf8 NOT NULL COMMENT 'è®¢å•å·',
  `completion_time` int(11) NOT NULL,
  `order_source` tinyint(1) NOT NULL DEFAULT '1' COMMENT 'è®¢å•æ¥æºï¼š1ï¼Œäº¬ä¸œ 2ï¼Œæ·˜å®',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=latin1 CHECKSUM=1 DELAY_KEY_WRITE=1 ROW_FORMAT=DYNAMIC;

/*Data for the table `taojin_order` */

insert  into `taojin_order`(`id`,`wx_bot`,`username`,`order_id`,`completion_time`,`order_source`) values (13,'跑堂优惠券','追梦的蚂蚁','73765263079',20180403,1);

/*Table structure for table `taojin_proxy_info` */

DROP TABLE IF EXISTS `taojin_proxy_info`;

CREATE TABLE `taojin_proxy_info` (
  `id` int(11) NOT NULL,
  `wx_bot` varchar(255) CHARACTER SET utf8 NOT NULL,
  `realname` varchar(32) CHARACTER SET utf8 DEFAULT NULL COMMENT 'ä»£ç†äººå§“å',
  `wx_bot_number` varchar(32) CHARACTER SET utf8 NOT NULL COMMENT 'æœºå™¨äººçš„å¾®ä¿¡å·',
  `jd_username` int(11) NOT NULL COMMENT 'äº¬ä¸œè”ç›Ÿè´¦å·',
  `jd_password` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT 'äº¬ä¸œè”ç›Ÿå¯†ç ',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Data for the table `taojin_proxy_info` */

/*Table structure for table `taojin_query_record` */

DROP TABLE IF EXISTS `taojin_query_record`;

CREATE TABLE `taojin_query_record` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `wx_bot` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '微信机器人',
  `good_title` varchar(255) CHARACTER SET utf8 NOT NULL,
  `good_price` decimal(10,2) NOT NULL,
  `good_coupon` int(10) DEFAULT NULL,
  `username` varchar(255) CHARACTER SET utf8 NOT NULL,
  `create_time` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=latin1 CHECKSUM=1 DELAY_KEY_WRITE=1 ROW_FORMAT=DYNAMIC;

/*Data for the table `taojin_query_record` */

insert  into `taojin_query_record`(`id`,`wx_bot`,`good_title`,`good_price`,`good_coupon`,`username`,`create_time`) values (2,'跑堂优惠券','万象更新多肉植物 花卉盆栽肉肉植物组合盆栽含花盆多肉土包邮','4.80',0,'彭波',1523467800),(3,'跑堂优惠券','【工厂直发】双倍辣韩国风味火鸡面干脆面整箱52g×48包干吃面国产方便面掌心脆掌心面网红零食团购批价 派力特火鸡干吃面整箱48包','36.90',0,'彭波',1523469923),(4,'跑堂优惠券','金沙河面粉 富强高筋小麦粉 馒头粉饺子粉 高筋烘焙原料面粉 5KG','19.90',0,'彭波',1523470025),(5,'跑堂优惠券','南极人短袖t恤男圆领韩版潮流学生外套男士半袖体恤宽松上衣夏季潮 黑白灰-可乐大叔/白虎/大满花 男170/M','119.00',0,'追梦的蚂蚁',1523499463),(6,'跑堂优惠券','金沙河面粉 富强高筋小麦粉 馒头粉饺子粉 高筋烘焙原料面粉 5KG','19.90',0,'彭波',1523499514),(7,'跑堂优惠券','【工厂直发】双倍辣韩国风味火鸡面干脆面整箱52g×48包干吃面国产方便面掌心脆掌心面网红零食团购批价 派力特火鸡干吃面整箱48包','36.90',0,'彭波',1523499543),(8,'跑堂优惠券','安踏男鞋板鞋2018春季韩版潮耐磨学生运动鞋男休闲鞋小白鞋 白黑 42','139.00',0,'追梦的蚂蚁',1523499592),(9,'跑堂优惠券','【工厂直发】双倍辣韩国风味火鸡面干脆面整箱52g×48包干吃面国产方便面掌心脆掌心面网红零食团购批价 派力特火鸡干吃面整箱48包','36.90',0,'彭波',1523499616),(10,'跑堂优惠券','毛衣马甲女短款春秋新款韩版V领坎肩毛线背心无袖针织衫外套春装','39.00',0,'追梦的蚂蚁',1523532373),(11,'跑堂优惠券','毛衣马甲女短款春秋新款韩版V领坎肩毛线背心无袖针织衫外套春装','39.00',0,'追梦的蚂蚁',1523715164),(12,'跑堂优惠券','韩国丝绒哑光唇釉染唇液豆沙色持久口红专柜正品同步销售','209.80',190,'彭波',1523717405),(13,'跑堂优惠券','2018新款纯棉时尚短袖t恤男 宽松半袖大码胖子加大号打底衫男款潮','49.99',25,'彭波',1523717487),(14,'跑堂优惠券','2018新款纯棉时尚短袖t恤男 宽松半袖大码胖子加大号打底衫男款潮','49.99',25,'彭波',1523717880),(15,'跑堂优惠券','2018新款纯棉时尚短袖t恤男 宽松半袖大码胖子加大号打底衫男款潮','49.99',25,'彭波',1523717996),(16,'跑堂优惠券','2018新款纯棉时尚短袖t恤男 宽松半袖大码胖子加大号打底衫男款潮','49.99',25,'彭波',1523718663),(17,'跑堂优惠券','2018新款纯棉时尚短袖t恤男 宽松半袖大码胖子加大号打底衫男款潮','49.99',25,'彭波',1523718691),(18,'跑堂优惠券','2018新款纯棉时尚短袖t恤男 宽松半袖大码胖子加大号打底衫男款潮','49.99',25,'彭波',1523724674),(19,'跑堂优惠券','2018新款纯棉时尚短袖t恤男 宽松半袖大码胖子加大号打底衫男款潮','49.99',25,'彭波',1523724694),(20,'跑堂优惠券','2018新款纯棉时尚短袖t恤男 宽松半袖大码胖子加大号打底衫男款潮','49.99',25,'彭波',1523724864),(21,'跑堂优惠券','2018新款纯棉时尚短袖t恤男 宽松半袖大码胖子加大号打底衫男款潮','49.99',25,'稳住，我们能赢',1523725246),(22,'跑堂优惠券','游戏超大大号鼠标垫锁边可爱动漫小号加厚笔记本电脑办公桌垫键盘','8.90',0,'追梦的蚂蚁',1523766983),(23,'跑堂优惠券','游戏超大大号鼠标垫锁边可爱动漫小号加厚笔记本电脑办公桌垫键盘','8.90',0,'追梦的蚂蚁',1523767090),(24,'跑堂优惠券','花花公子贵宾夹克男外套 2018春季新品薄款修身男装外套 2801黑色 4XL','139.00',5,'追梦的蚂蚁',1523767511),(25,'跑堂优惠券','花花公子贵宾夹克男外套 2018春季新品薄款修身男装外套 2801黑色 4XL','139.00',5,'彭波',1523767534),(26,'跑堂优惠券','2018新款纯棉时尚短袖t恤男 宽松半袖大码胖子加大号打底衫男款潮','49.99',25,'彭波',1523767573),(27,'跑堂优惠券','金沙河面粉 富强高筋小麦粉 馒头粉饺子粉 高筋烘焙原料面粉 5KG','19.90',0,'追梦的蚂蚁',1523772193),(28,'跑堂优惠券','得力(deli)色泽明亮可擦易擦白板笔 黑色 10支/盒6817','12.00',0,'追梦的蚂蚁',1523773815),(29,'跑堂优惠券','花花公子贵宾夹克男外套 2018春季新品薄款修身男装外套 2801黑色 4XL','139.00',5,'彭波',1523792130),(30,'跑堂优惠券','花花公子贵宾夹克男外套 2018春季新品薄款修身男装外套 2801黑色 4XL','139.00',5,'彭波',1523798474),(31,'跑堂优惠券','2018新款纯棉时尚短袖t恤男 宽松半袖大码胖子加大号打底衫男款潮','49.99',25,'彭波',1523798493),(32,'跑堂优惠券','2018新款纯棉时尚短袖t恤男 宽松半袖大码胖子加大号打底衫男款潮','49.99',25,'彭波',1523798541),(33,'跑堂优惠券','2018新款纯棉时尚短袖t恤男 宽松半袖大码胖子加大号打底衫男款潮','49.99',25,'彭波',1523798707),(34,'跑堂优惠券','2018新款纯棉时尚短袖t恤男 宽松半袖大码胖子加大号打底衫男款潮','49.99',25,'彭波',1523799809),(35,'跑堂优惠券','2018新款纯棉时尚短袖t恤男 宽松半袖大码胖子加大号打底衫男款潮','49.99',25,'彭波',1523800877),(36,'跑堂优惠券','2018新款纯棉时尚短袖t恤男 宽松半袖大码胖子加大号打底衫男款潮','49.99',25,'彭波',1523801115),(37,'跑堂优惠券','2018新款纯棉时尚短袖t恤男 宽松半袖大码胖子加大号打底衫男款潮','49.99',25,'彭波',1523801146),(38,'跑堂优惠券','2018新款纯棉时尚短袖t恤男 宽松半袖大码胖子加大号打底衫男款潮','49.99',25,'彭波',1523801680),(39,'跑堂优惠券','TEEK 短袖T恤男春夏季新款 男士半袖体恤衣服 修身男装打底衫 浅红色 175/96A(L码)','79.00',0,'追梦的蚂蚁',1523803770),(40,'跑堂优惠券','TEEK 短袖T恤男春夏季新款 男士半袖体恤衣服 修身男装打底衫 浅红色 175/96A(L码)','79.00',0,'追梦的蚂蚁',1523806347),(41,'跑堂优惠券','花花公子贵宾夹克男外套 2018春季新品薄款修身男装外套 2801黑色 4XL','139.00',5,'彭波',1523809817),(42,'追梦的蚂蚁','南极人短袖t恤男圆领韩版潮流学生外套男士半袖体恤宽松上衣夏季潮 黑白灰-可乐大叔/白虎/大满花 男170/M','119.00',0,'666的小号',1523897364),(43,'追梦的蚂蚁','南极人短袖t恤男圆领韩版潮流学生外套男士半袖体恤宽松上衣夏季潮 黑白灰-可乐大叔/白虎/大满花 男170/M','119.00',0,'666的小号',1523899085),(44,'追梦的蚂蚁','卫衣男连帽春秋韩版潮流学生ins套头上衣宽松运动bf帅气男士外套','89.00',0,'666的小号',1523899100),(45,'追梦的蚂蚁','鳄鱼恤短袖T恤男士夏季休闲衣服圆领潮流印花衣服打底T恤半袖男装 md832 灰色 L','99.00',0,'666的小号',1524145873),(46,'追梦的蚂蚁','ins格子衬衫外套男士衬衣长袖韩版潮流春秋夏季文艺港风原宿休闲','55.00',0,'666的小号',1524577503),(47,'追梦的蚂蚁','ins格子衬衫外套男士衬衣长袖韩版潮流春秋夏季文艺港风原宿休闲','55.00',0,'666的小号',1524577721),(48,'追梦的蚂蚁','ins格子衬衫外套男士衬衣长袖韩版潮流春秋夏季文艺港风原宿休闲','55.00',0,'666的小号',1524577841);

/*Table structure for table `taojin_rebate_log` */

DROP TABLE IF EXISTS `taojin_rebate_log`;

CREATE TABLE `taojin_rebate_log` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `wx_bot` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '机器人',
  `username` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT 'ç”¨æˆ·',
  `rebate_amount` float(11,2) NOT NULL,
  `type` tinyint(1) NOT NULL COMMENT 'è¿”åˆ©ç±»åž‹ï¼š1æ·»åŠ æœºå™¨äººè¿”åˆ©ï¼Œ2é‚€è¯·äººè¿”åˆ©ï¼Œ3ï¼Œè´­ç‰©è¿”åˆ©ï¼Œ4é‚€è¯·äººè´­ç‰©è¿”åˆ©',
  `create_time` int(11) NOT NULL COMMENT 'åˆ›å»ºæ—¶é—´',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=latin1 CHECKSUM=1 DELAY_KEY_WRITE=1 ROW_FORMAT=DYNAMIC;

/*Data for the table `taojin_rebate_log` */

insert  into `taojin_rebate_log`(`id`,`wx_bot`,`username`,`rebate_amount`,`type`,`create_time`) values (6,'跑堂优惠券','彭波',0.30,1,1523467672),(7,'跑堂优惠券','彭波',0.07,3,1523468330),(8,'跑堂优惠券','彭波',0.07,3,1523468879),(9,'跑堂优惠券','彭波',0.07,3,1523469184),(10,'跑堂优惠券','彭波',0.07,3,1523469446),(11,'跑堂优惠券','彭波',0.07,3,1523469479),(12,'跑堂优惠券','彭波',0.07,3,1523469670),(13,'跑堂优惠券','彭波',0.07,3,1523469750),(14,'跑堂优惠券','追梦的蚂蚁',0.30,1,1523499462),(15,'跑堂优惠券','666的小号',0.30,1,1523499639),(16,'跑堂优惠券','追梦的蚂蚁',0.30,2,1523499639),(17,'跑堂优惠券','追梦的蚂蚁',0.00,3,1523772470),(18,'跑堂优惠券','追梦的蚂蚁',0.00,3,1523773041),(19,'跑堂优惠券','追梦的蚂蚁',0.00,3,1523773184),(20,'跑堂优惠券','追梦的蚂蚁',0.00,3,1523773405),(21,'跑堂优惠券','追梦的蚂蚁',0.03,3,1523773825),(22,'跑堂优惠券','追梦的蚂蚁',0.03,3,1523774236),(23,'跑堂优惠券','追梦的蚂蚁',0.03,3,1523774392),(24,'跑堂优惠券','追梦的蚂蚁',0.03,3,1523776033),(25,'跑堂优惠券','彭波',0.01,4,1523776033),(26,'跑堂优惠券','追梦的蚂蚁',0.03,3,1523777318),(27,'跑堂优惠券','彭波',0.01,4,1523777318),(28,'跑堂优惠券','追梦的蚂蚁',0.03,3,1523778861),(29,'跑堂优惠券','彭波',0.01,4,1523778862),(30,'跑堂优惠券','追梦的蚂蚁',0.03,3,1523804154),(31,'跑堂优惠券','彭波',0.01,4,1523804154),(32,'追梦的蚂蚁','666的小号',0.30,1,1523897363),(33,'追梦的蚂蚁','跑堂优惠券',0.30,1,1524146379);

/*Table structure for table `taojin_user_info` */

DROP TABLE IF EXISTS `taojin_user_info`;

CREATE TABLE `taojin_user_info` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `wx_bot` varchar(255) NOT NULL COMMENT '机器人',
  `wx_number` varchar(255) NOT NULL COMMENT 'å¾®ä¿¡å·',
  `sex` tinyint(1) NOT NULL DEFAULT '1' COMMENT 'æ€§åˆ«,1ç”·ï¼Œ2å¥³',
  `nickname` varchar(255) NOT NULL,
  `lnivt_code` varchar(255) NOT NULL DEFAULT '0',
  `total_rebate_amount` float(11,2) unsigned NOT NULL DEFAULT '0.00' COMMENT 'æ€»è¿”åˆ©é‡‘é¢',
  `jd_rebate_amount` float(11,2) NOT NULL DEFAULT '0.00' COMMENT 'äº¬ä¸œè¿”åˆ©',
  `taobao_rebate_amount` float(11,2) unsigned NOT NULL DEFAULT '0.00' COMMENT 'æ·˜å®è¿”åˆ©é‡‘é¢',
  `withdrawals_amount` float(11,2) unsigned NOT NULL DEFAULT '0.00' COMMENT 'å¾…æçŽ°é‡‘é¢',
  `save_money` float(11,2) unsigned NOT NULL DEFAULT '0.00' COMMENT 'å…±èŠ‚çœé‡‘é¢',
  `order_quantity` int(11) unsigned NOT NULL DEFAULT '0' COMMENT 'è®¢å•æ€»æ•°é‡',
  `jd_order_quantity` int(11) unsigned NOT NULL DEFAULT '0' COMMENT 'äº¬ä¸œè®¢å•æ•°é‡',
  `taobao_order_quantity` int(11) NOT NULL DEFAULT '0' COMMENT 'æ·˜å®è®¢å•æ•°é‡',
  `jd_completed_order` int(11) NOT NULL DEFAULT '0' COMMENT 'äº¬ä¸œå·²å®Œæˆè®¢å•æ•°é‡',
  `taobao_completed_order` int(11) NOT NULL DEFAULT '0' COMMENT 'æ·˜å®å·²å®Œæˆè®¢å•æ•°é‡',
  `jd_unfinished_order` int(11) NOT NULL DEFAULT '0' COMMENT 'äº¬ä¸œæœªå®Œæˆè®¢å•æ•°é‡',
  `lnivter` varchar(255) NOT NULL DEFAULT '0' COMMENT 'é‚€è¯·äºº',
  `taobao_unfinished_order` int(11) NOT NULL DEFAULT '0' COMMENT 'æ·˜å®æœªå®Œæˆè®¢å•æ•°é‡',
  `friends_rebate` float(11,2) NOT NULL DEFAULT '0.00' COMMENT 'å¥½å‹è¿”åˆ©é‡‘é¢',
  `friends_number` int(11) NOT NULL DEFAULT '0' COMMENT 'ä¸‹çº¿ä¸ªæ•°',
  `create_time` int(11) NOT NULL DEFAULT '0' COMMENT 'åˆ›å»ºæ—¶é—´',
  `update_time` int(11) DEFAULT NULL COMMENT 'æ›´æ–°æ—¶é—´',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8 CHECKSUM=1 DELAY_KEY_WRITE=1 ROW_FORMAT=DYNAMIC;

/*Data for the table `taojin_user_info` */

insert  into `taojin_user_info`(`id`,`wx_bot`,`wx_number`,`sex`,`nickname`,`lnivt_code`,`total_rebate_amount`,`jd_rebate_amount`,`taobao_rebate_amount`,`withdrawals_amount`,`save_money`,`order_quantity`,`jd_order_quantity`,`taobao_order_quantity`,`jd_completed_order`,`taobao_completed_order`,`jd_unfinished_order`,`lnivter`,`taobao_unfinished_order`,`friends_rebate`,`friends_number`,`create_time`,`update_time`) values (4,'跑堂优惠券','彭波',1,'彭波','0',0.49,0.00,0.49,0.79,2.45,7,0,7,0,0,0,'0',0,0.01,0,1523467672,1523804154),(5,'跑堂优惠券','追梦的蚂蚁',1,'追梦的蚂蚁','wxid_wwixw6bnpee422',1.52,0.21,0.00,0.00,0.00,4,4,0,0,0,0,'0',0,0.00,1,1523499461,1523805351),(6,'跑堂优惠券','666的小号',1,'666的小号','wxid_12ebjj9idjw222',0.00,0.00,0.00,0.30,0.00,0,0,0,0,0,0,'wxid_wwixw6bnpee422',0,0.00,0,1523499638,NULL),(7,'追梦的蚂蚁','666的小号',1,'666的小号','0',0.00,0.00,0.00,0.30,0.00,0,0,0,0,0,0,'0',0,0.00,0,1523897363,NULL),(8,'追梦的蚂蚁','跑堂优惠券',0,'跑堂优惠券','wxid_rssh7e0xk9vm12',0.00,0.00,0.00,0.30,0.00,0,0,0,0,0,0,'0',0,0.00,0,1524146379,NULL);

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
