# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.users import Users
from datetime import datetime

class Accountings(BaseModel):
    description = TextField(null=True)
    createTime = DateTimeField(default=datetime.now)
    owner = ForeignKeyField(Users, related_name='accountings_owner', on_delete='CASCADE')
    status = IntegerField(default=0)
    remark = TextField(null=True)
    # 上个月未结账金额
    symwjzje = CharField(null=True)
    # 本月发货合计
    byfhhj = CharField(null=True)
    # 本月到账合计
    bydzhj = CharField(null=True)
    # 月末结存
    ymjc = CharField(null=True)
    # 本月业务利润
    byywlr = CharField(null=True)
    # 本月开票
    bykp = CharField(null=True)
    # 本月奖
    byj = CharField(null=True)
    # 本月扣
    byk = CharField(null=True)
    # 本年发货累计
    bnfhlj = CharField(null=True)
    # 本年到账累计
    bndzlj = CharField(null=True)
