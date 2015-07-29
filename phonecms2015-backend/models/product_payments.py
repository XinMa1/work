# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.users import Users
from models.products import Products
from models.transactions import Transactions
from datetime import datetime

class ProductPayments(BaseModel):
    product = ForeignKeyField(Products, related_name='product_payments', on_delete='CASCADE')
    created_time = TimeField(formats="%Y-%m-%d %H:%M:%S",
            default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    remark = TextField(null=True)
    transaction = ForeignKeyField(Transactions, related_name='product_payments_transaction', on_delete='CASCADE')
