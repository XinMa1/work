# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.accountings import Accountings
from datetime import datetime

class AccountIncommings(BaseModel):
    description = TextField(null=True)
    createTime = DateTimeField(default=datetime.now) 
    # 金额
    money = FloatField()
    # 来款单位
    origin = CharField()
    # 对账
    accounting = ForeignKeyField(Accountings, related_name='incommings_account', on_delete='CASCADE')
