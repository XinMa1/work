# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.images import Images
from models.categories import Categories
from datetime import datetime

class Articles(BaseModel):
    name = CharField(unique=True)
    thumbnail = ForeignKeyField(Images, related_name='articles_thumbnail', on_delete='CASCADE')
    category = ForeignKeyField(Categories, related_name='articles_category', on_delete='CASCADE')
    content = TextField()
    createTime = DateTimeField(default=datetime.now) 
