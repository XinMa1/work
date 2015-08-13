# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel

class Categories(BaseModel):
    name = CharField(unique=True)
    description = TextField()
    #Self-referential foreign keys should always be null=True.
    parent = ForeignKeyField('self', null=True, related_name='children')
