# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.images import Images
from models.users import Users
from datetime import datetime

class Notifications(BaseModel):
    name = CharField(unique=True)
    thumbnail = ForeignKeyField(Images, related_name='notifications_thumbnail', on_delete='CASCADE')
    content = TextField(null=True)
    createTime = DateTimeField(default=datetime.now)
    emoji = TextField(null=True) 
