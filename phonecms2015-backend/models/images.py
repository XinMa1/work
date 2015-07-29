# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from datetime import datetime
from models.base import BaseModel
from models.users import Users
from models.albums import Albums

class Images(BaseModel):
    uuid = CharField(unique=True)
    link = CharField(null=True)
    created_time = DateTimeField(default=datetime.now)
    description = TextField(null=True)
    thumbnail = TextField()
    owner = ForeignKeyField(Users, related_name='images_owner', on_delete='CASCADE')
    album = ForeignKeyField(Albums, related_name='images', on_delete='CASCADE')
