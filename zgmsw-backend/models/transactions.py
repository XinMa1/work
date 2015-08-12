# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.users import Users
from models.courses import Courses
from datetime import datetime

class Transactions(BaseModel):
    description = TextField(null=True)
    created_time = TimeField(formats="%Y-%m-%d %H:%M:%S",
            default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    last_modified_time = TimeField(formats="%Y-%m-%d %H:%M:%S",
            default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    last_callback_time = TimeField(formats="%Y-%m-%d %H:%M:%S",
            default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    trade_id = CharField(unique=True)
    alipay_trade_id = CharField(null=True)
    trade_status = IntegerField(null=True)
    total_price = FloatField(default=.0)
    owner = ForeignKeyField(Users, related_name='transactions_owner', on_delete='CASCADE')

class TransactionStatus:
    STATUS_NONE=0
    STATUS_WAITPAY=1
    STATUS_COMPLETE=2
    STATUS_ERROR=3

    @classmethod
    def statusName(cls, status):
       try:
           status = int(status)
           if status == cls.STATUS_NONE or status == cls.STATUS_WAITPAY:
               return "待付款"
           elif status == cls.STATUS_COMPLETE:
               return "已付款"
           elif status == cls.STATUS_ERROR:
               return "错误"
           else:
               return "未知"
       except Exception as e:
           return "未知"
