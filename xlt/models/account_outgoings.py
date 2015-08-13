# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.users import Users
from models.accountings import Accountings
from datetime import datetime

class AccountOutgoings(BaseModel):
    description = TextField(null=True)
    createTime = DateTimeField(default=datetime.now) 
    # 金额
    money = FloatField()
    # 盘数
    count = IntegerField()
    # 对账
    accounting = ForeignKeyField(Accountings, related_name='outgoings_account', on_delete='CASCADE')
