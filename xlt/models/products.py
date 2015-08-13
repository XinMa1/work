# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.categories import Categories

class Products(BaseModel):
    name = CharField()
    description = TextField(null=True)
    # 铝芯，铜芯
    type = IntegerField()
    # 直径
    diameter = CharField()
    # 厂标价格
    price1 = FloatField(null=True)
    # 国标价格
    price2 = FloatField(null=True)
    # 所属分类
    category = ForeignKeyField(Categories, related_name='products_category', on_delete='CASCADE')
