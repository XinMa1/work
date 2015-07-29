# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.users import Users
from models.images import Images

class Chatrooms(BaseModel):
    name = CharField()
    description = TextField(null=True)
    thumbnail = ForeignKeyField(Images, related_name='chatrooms_thumbnail', on_delete='CASCADE')
    uuid = TextField(null=True)
    owner = ForeignKeyField(Users, related_name='chatrooms_owner', on_delete='CASCADE')
