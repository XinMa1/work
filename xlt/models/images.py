# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from datetime import datetime
from models.base import BaseModel

class Images(BaseModel):
    uuid = CharField(unique=True)
    link = CharField(null=True)
    created_time = DateTimeField(default=datetime.now)
    description = TextField(null=True)
    thumbnail = TextField()
