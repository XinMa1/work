# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.products import Products
from models.orders import Orders

class OrderDetails(BaseModel):
    #对应于产品的分类名称
    name = TextField()
    description = TextField(null=True)
    product = ForeignKeyField(Products, related_name='orders_product', on_delete='CASCADE')
    order = ForeignKeyField(Orders, related_name='products_order', on_delete='CASCADE')
    count = IntegerField(default=1)
    price = FloatField(null=True)
    # 利润率
    ratio = FloatField(default=0.0)
    #默认为国标或者厂标价，否则为自定义价
    flag = BooleanField(default=False)
