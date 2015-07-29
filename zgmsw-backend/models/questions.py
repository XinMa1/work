# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.users import Users
from models.albums import Albums
from models.groups import Groups
from datetime import datetime

class Questions(BaseModel):
    title = CharField()
    #问题类型，扩展作用
    type = CharField(default=1)
    # 问题开放1 关闭 0
    status = CharField(default=1)
    created_time = DateTimeField(default=datetime.now)
    content = TextField(null=True)
    owner = ForeignKeyField(Users, related_name='questions_owner', on_delete='CASCADE')
    group = ForeignKeyField(Groups, related_name='questions_group', on_delete='CASCADE')
    album = ForeignKeyField(Albums, null=True, related_name='questions_album', on_delete='CASCADE')
