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
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1;

/*Table structure for table `taojin_good_info` */

DROP TABLE IF EXISTS `taojin_good_info`;

CREATE TABLE `taojin_good_info` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
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
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=latin1 CHECKSUM=1 DELAY_KEY_WRITE=1 ROW_FORMAT=DYNAMIC;

/*Table structure for table `taojin_group_message` */

DROP TABLE IF EXISTS `taojin_group_message`;

CREATE TABLE `taojin_group_message` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '机器人名称',
  `groupid` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '群id',
  `groupname` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '群名称',
  `create_time` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=51 DEFAULT CHARSET=latin1;

/*Table structure for table `taojin_order` */

DROP TABLE IF EXISTS `taojin_order`;

CREATE TABLE `taojin_order` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT 'ç”¨æˆ·å',
  `order_id` char(32) NOT NULL COMMENT 'è®¢å•å·',
  `order_source` tinyint(1) NOT NULL DEFAULT '1' COMMENT 'è®¢å•æ¥æºï¼š1ï¼Œäº¬ä¸œ 2ï¼Œæ·˜å®',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `taojin_proxy_info` */

DROP TABLE IF EXISTS `taojin_proxy_info`;

CREATE TABLE `taojin_proxy_info` (
  `id` int(11) NOT NULL,
  `realname` varchar(32) DEFAULT NULL COMMENT 'ä»£ç†äººå§“å',
  `wx_bot_number` varchar(32) NOT NULL COMMENT 'æœºå™¨äººçš„å¾®ä¿¡å·',
  `jd_username` int(11) NOT NULL COMMENT 'äº¬ä¸œè”ç›Ÿè´¦å·',
  `jd_password` varchar(255) NOT NULL COMMENT 'äº¬ä¸œè”ç›Ÿå¯†ç ',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

/*Table structure for table `taojin_query_record` */

DROP TABLE IF EXISTS `taojin_query_record`;

CREATE TABLE `taojin_query_record` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `good_title` varchar(255) CHARACTER SET utf8 NOT NULL,
  `good_price` decimal(10,2) NOT NULL,
  `good_coupon` int(10) DEFAULT NULL,
  `username` varchar(255) CHARACTER SET utf8 NOT NULL,
  `create_time` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=122 DEFAULT CHARSET=latin1;

/*Table structure for table `taojin_rebate_log` */

DROP TABLE IF EXISTS `taojin_rebate_log`;

CREATE TABLE `taojin_rebate_log` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `username` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT 'ç”¨æˆ·',
  `rebate_amount` float(11,2) NOT NULL,
  `type` tinyint(1) NOT NULL COMMENT 'è¿”åˆ©ç±»åž‹ï¼š1æ·»åŠ æœºå™¨äººè¿”åˆ©ï¼Œ2é‚€è¯·äººè¿”åˆ©ï¼Œ3ï¼Œè´­ç‰©è¿”åˆ©ï¼Œ4é‚€è¯·äººè´­ç‰©è¿”åˆ©',
  `create_time` int(11) NOT NULL COMMENT 'åˆ›å»ºæ—¶é—´',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=94 DEFAULT CHARSET=latin1;

/*Table structure for table `taojin_user_info` */

DROP TABLE IF EXISTS `taojin_user_info`;

CREATE TABLE `taojin_user_info` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `wx_number` varchar(255) NOT NULL COMMENT 'å¾®ä¿¡å·',
  `sex` tinyint(1) NOT NULL DEFAULT '1' COMMENT 'æ€§åˆ«,1ç”·ï¼Œ2å¥³',
  `nickname` varchar(255) NOT NULL,
  `lnivt_code` int(11) unsigned NOT NULL DEFAULT '0' COMMENT 'é‚€è¯·ç ',
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
  `lnivter` int(11) DEFAULT NULL COMMENT 'é‚€è¯·äºº',
  `taobao_unfinished_order` int(11) NOT NULL DEFAULT '0' COMMENT 'æ·˜å®æœªå®Œæˆè®¢å•æ•°é‡',
  `friends_rebate` float(11,2) NOT NULL DEFAULT '0.00' COMMENT 'å¥½å‹è¿”åˆ©é‡‘é¢',
  `friends_number` int(11) NOT NULL DEFAULT '0' COMMENT 'ä¸‹çº¿ä¸ªæ•°',
  `create_time` int(11) NOT NULL DEFAULT '0' COMMENT 'åˆ›å»ºæ—¶é—´',
  `update_time` int(11) DEFAULT NULL COMMENT 'æ›´æ–°æ—¶é—´',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8 CHECKSUM=1 DELAY_KEY_WRITE=1 ROW_FORMAT=DYNAMIC;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
