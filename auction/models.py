# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
import datetime

# Create your models here.

class Show(models.Model):
    """
    演出信息包括:
    演出名称-时间(多次)-地点-票等级-大麦网连接
    由爬虫产出,选择时选择已有场次和票价,在买入/卖出时有优势
    """
    show_id = models.CharField(max_length=100, primary_key=True)
    show_name = models.CharField(max_length=100)
    play_time = models.CharField(max_length=100) # 时间数组格式
    position = models.CharField(max_length=100)
    price_choices = models.CharField(max_length=100) # 票价数组格式
    damai_url = models.CharField(max_length=100)    # 大麦网连接地址

class Action_User(models.Model):
    """
    用户只需要用户名,地址,帐户余额
    """
    user_id = models.CharField(max_length=30, unique=True, primary_key=True)
    address = models.CharField(max_length=300)
    wallet = models.FloatField()


class Category(models.Model):
    category = models.CharField(max_length=20, primary_key=True)

class SellCase(models.Model):
    """
    发布卖出信息的订单包含的信息。卖出者视图
    goods: 所有
    """
    show = models.ForeignKey(Show)
    sell_case_id = models.PositiveIntegerField(primary_key=True)
    online_price = models.IntegerField(default=0)
    offline_price = models.IntegerField(default=0)
    description = models.TextField(default="")
    category = models.ForeignKey(Category, related_name='category_goods')
    online_time = models.DateTimeField(default=datetime.datetime.now())
    seller = models.ForeignKey(Action_User)
    separate_sell = models.CharField(max_length=255, default="")
    net_ticket_code = models.CharField(max_length=255, default="")
    lianzuo = models.CharField(max_length=255, default="")
    peisongfangshi = models.CharField(max_length=255, default="")


class BuyCase(models.Model):
    """
    发布买入信息的订单包含的信息。买入者视图
    """
    buy_case_id = models.PositiveIntegerField(primary_key=True)
    online_price = models.PositiveIntegerField()
    offline_price = models.PositiveIntegerField()
    description = models.TextField()
    buyer = models.ForeignKey(Action_User)
    show = models.ForeignKey(Show)
    lianzuo = models.CharField(max_length=100, default="")
    ticket_num = models.IntegerField(default=0)

class Deal(models.Model):
    """
    成交的订单的信息,内部可见。联系卖出,买入者视图
    """
    deal_id = models.PositiveIntegerField(unique=True, primary_key=True)
    deal_time = models.DateTimeField(auto_now=True)
    # 成交价格
    deal_price = models.PositiveIntegerField()
    buy_case = models.ForeignKey(BuyCase)


class Goods(models.Model):
    """
    可以单独交易的最小单位。一个卖出/买入订单可以分解成1个/多个单独的物品买入/卖出
    暂时只表示票据
    """
    goods_id = models.CharField(max_length=30, unique=True, primary_key=True)
    goods_name = models.CharField(max_length=30,default="")
    offline_time = models.DateTimeField()

    PREPARE = "PREPARE"
    ONSALE = 'ONSALE'
    EXPIRE = 'EXPIRE'
    OFFLINE = "OFFLINE"

    STATUS = (
        (PREPARE, "PREPARE"),
        (ONSALE, 'ONSALE'),
        (EXPIRE, 'EXPIRE'),
        (OFFLINE, 'OFFLINE')
    )
    status = models.CharField(max_length=20, choices=STATUS, default=PREPARE)
    deal_price = models.FloatField(default=0.0)
    org_price = models.FloatField(default=0.0)
    sit_num = models.CharField(max_length=200, default="")
    sell_case = models.ForeignKey(SellCase)
    deal_case_id = models.CharField(max_length=20)
    show_id = models.CharField(max_length=20)
    online_price = models.IntegerField(default=0)
    offline_price = models.IntegerField(default=0)