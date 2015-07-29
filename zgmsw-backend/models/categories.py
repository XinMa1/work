# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.users import Users

class Categories(BaseModel):
    name = CharField(null = True)
    thumbnail = TextField()
    description = TextField()
    #Self-referential foreign keys should always be null=True.
    parentName = CharField(null = True)
    parent = ForeignKeyField('self', null=True, related_name='children')
