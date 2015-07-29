# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.users import Users

class Albums(BaseModel):
    name = CharField(unique=True)
    description = TextField()
    thumbnail = TextField()
    owner = ForeignKeyField(Users, related_name='albums_owner', on_delete='CASCADE')
