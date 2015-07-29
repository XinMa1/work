# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.users import Users
from models.products import Products
from datetime import datetime

class ProductRankings(BaseModel):
    type = IntegerField()
    value = IntegerField(default=4)
    owner = ForeignKeyField(Users, related_name='product_rankings_owner', on_delete='CASCADE')
    product = ForeignKeyField(Products, related_name='product_rankings', on_delete='CASCADE')
    created_time = DateTimeField(default=datetime.now)
