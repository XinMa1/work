# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.users import Users
from models.groups import Groups
from models.transactions import Transactions

from datetime import datetime

class GroupPayments(BaseModel):
    group = ForeignKeyField(Groups, related_name='group_payments', on_delete='CASCADE')
    created_time = TimeField(formats="%Y-%m-%d %H:%M:%S",
            default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    remark = TextField(null=True)
    type = IntegerField(default=0)
    transaction = ForeignKeyField(Transactions, related_name='group_payments_transaction')
