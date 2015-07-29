# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.users import Users
from models.groups import Groups
from datetime import datetime

class GroupComments(BaseModel):
    owner = ForeignKeyField(Users, related_name='group_comments_owner', on_delete='CASCADE')
    group = ForeignKeyField(Groups, related_name='group_comments', on_delete='CASCADE')
    created_time = DateTimeField(default=datetime.now)
    content = TextField(null=True)
    value = IntegerField(default=4)
