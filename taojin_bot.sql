/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50505
Source Host           : localhost:3306
Source Database       : taojin_bot

Target Server Type    : MYSQL
Target Server Version : 50505
File Encoding         : 65001

Date: 2018-03-26 09:38:39
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for taojin_current_log
-- ----------------------------
DROP TABLE IF EXISTS `taojin_current_log`;
CREATE TABLE `taojin_current_log` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `wx_bot` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '微信机器人',
  `username` varchar(255) CHARACTER SET utf8 NOT NULL DEFAULT '0' COMMENT '提现人',
  `amount` float(11,2) NOT NULL DEFAULT '1.00' COMMENT '提现金额',
  `create_time` int(11) NOT NULL COMMENT '提现时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for taojin_order
-- ----------------------------
DROP TABLE IF EXISTS `taojin_order`;
CREATE TABLE `taojin_order` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '用户名',
  `order_id` char(32) NOT NULL COMMENT '订单号',
  `order_source` tinyint(1) NOT NULL DEFAULT '1' COMMENT '订单来源：1，京东 2，淘宝',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for taojin_proxy_info
-- ----------------------------
DROP TABLE IF EXISTS `taojin_proxy_info`;
CREATE TABLE `taojin_proxy_info` (
  `id` int(11) NOT NULL,
  `realname` varchar(32) DEFAULT NULL COMMENT '代理人姓名',
  `wx_bot_number` varchar(32) NOT NULL COMMENT '机器人的微信号',
  `jd_username` int(11) NOT NULL COMMENT '京东联盟账号',
  `jd_password` varchar(255) NOT NULL COMMENT '京东联盟密码',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for taojin_query_record
-- ----------------------------
DROP TABLE IF EXISTS `taojin_query_record`;
CREATE TABLE `taojin_query_record` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `good_title` varchar(255) CHARACTER SET utf8 NOT NULL,
  `good_price` decimal(10,2) NOT NULL,
  `good_coupon` int(10) DEFAULT NULL,
  `username` varchar(255) CHARACTER SET utf8 NOT NULL,
  `create_time` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for taojin_rebate_log
-- ----------------------------
DROP TABLE IF EXISTS `taojin_rebate_log`;
CREATE TABLE `taojin_rebate_log` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT COMMENT 'id',
  `username` varchar(255) CHARACTER SET utf8 NOT NULL COMMENT '用户',
  `rebate_amount` float(11,2) NOT NULL,
  `type` tinyint(1) NOT NULL COMMENT '返利类型：1添加机器人返利，2邀请人返利，3，购物返利，4邀请人购物返利',
  `create_time` int(11) NOT NULL COMMENT '创建时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=62 DEFAULT CHARSET=latin1;

-- ----------------------------
-- Table structure for taojin_user_info
-- ----------------------------
DROP TABLE IF EXISTS `taojin_user_info`;
CREATE TABLE `taojin_user_info` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `wx_number` varchar(255) NOT NULL COMMENT '微信号',
  `sex` tinyint(1) NOT NULL DEFAULT '1' COMMENT '性别,1男，2女',
  `nickname` varchar(255) NOT NULL,
  `lnivt_code` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '邀请码',
  `total_rebate_amount` float(11,2) unsigned NOT NULL DEFAULT '0.00' COMMENT '总返利金额',
  `jd_rebate_amount` float(11,2) NOT NULL DEFAULT '0.00' COMMENT '京东返利',
  `taobao_rebate_amount` float(11,2) unsigned NOT NULL DEFAULT '0.00' COMMENT '淘宝返利金额',
  `withdrawals_amount` float(11,2) unsigned NOT NULL DEFAULT '0.00' COMMENT '待提现金额',
  `save_money` float(11,2) unsigned NOT NULL DEFAULT '0.00' COMMENT '共节省金额',
  `order_quantity` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '订单总数量',
  `jd_order_quantity` int(11) unsigned NOT NULL DEFAULT '0' COMMENT '京东订单数量',
  `taobao_order_quantity` int(11) NOT NULL DEFAULT '0' COMMENT '淘宝订单数量',
  `jd_completed_order` int(11) NOT NULL DEFAULT '0' COMMENT '京东已完成订单数量',
  `taobao_completed_order` int(11) NOT NULL DEFAULT '0' COMMENT '淘宝已完成订单数量',
  `jd_unfinished_order` int(11) NOT NULL DEFAULT '0' COMMENT '京东未完成订单数量',
  `lnivter` int(11) DEFAULT NULL COMMENT '邀请人',
  `taobao_unfinished_order` int(11) NOT NULL DEFAULT '0' COMMENT '淘宝未完成订单数量',
  `friends_rebate` float(11,2) NOT NULL DEFAULT '0.00' COMMENT '好友返利金额',
  `friends_number` int(11) NOT NULL DEFAULT '0' COMMENT '下线个数',
  `create_time` int(11) NOT NULL DEFAULT '0' COMMENT '创建时间',
  `update_time` int(11) DEFAULT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8 ROW_FORMAT=COMPACT;
