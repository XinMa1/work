# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.users import Users
from models.products import Products
from datetime import datetime

class ProductFavorites(BaseModel):
    owner = ForeignKeyField(Users, related_name='product_favorites_owner', on_delete='CASCADE')
    product = ForeignKeyField(Products, related_name='product_favorites', on_delete='CASCADE')
    created_time = DateTimeField(default=datetime.now)
