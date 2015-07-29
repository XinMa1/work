# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.users import Users
from models.articles import Articles
from datetime import datetime

class ArticleFavorites(BaseModel):
    owner = ForeignKeyField(Users, related_name='article_favorites_owner', on_delete='CASCADE')
    article = ForeignKeyField(Articles, related_name='article_favorites', on_delete='CASCADE')
    created_time = DateTimeField(default=datetime.now)
