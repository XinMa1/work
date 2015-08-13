# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.users import Users
from datetime import datetime

class Orders(BaseModel):
    description = TextField(null=True)
    created_time = DateTimeField(default=datetime.now)
    owner = ForeignKeyField(Users, related_name='orders_owner', on_delete='CASCADE')
    price = FloatField()
    customer = CharField(default='未知公司')
