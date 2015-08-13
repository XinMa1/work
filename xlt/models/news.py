# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.images import Images
from datetime import datetime

class News(BaseModel):
    name = CharField(unique=True)
    thumbnail = ForeignKeyField(Images, related_name='news_thumbnail', on_delete='CASCADE')
    content = TextField()
    createTime = DateTimeField(default=datetime.now) 
