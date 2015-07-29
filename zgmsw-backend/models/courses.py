# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.users import Users
from models.categories import Categories
from models.groups import Groups
from models.images import Images
from datetime import datetime

class Courses(BaseModel):
    name = CharField(unique=True)
    # 1. 录播
    # 2. 直播
    type = CharField(default=1)
    price = FloatField(default=.0)
    discount = FloatField(default=.0)
    created_time = DateTimeField(default=datetime.now)
    video_name = TextField(null = True)
    video_desc = TextField(null = True)
    video_url = TextField(null = True)
    video_mobile_url = TextField(null=True)
    video_adaptive_url = TextField(null=True)
    video_rate = TextField(null=True)
    video_width =  IntegerField(null=True)
    video_height = IntegerField(null=True)
    video_thumbnail = TextField(null=True)
    video_uptime = TextField(null=True)
    video_duration = TextField(null=True)
    description = TextField(null=True)
    thumbnail = ForeignKeyField(Images, related_name='courses_thumbnail')
    is_star = BooleanField(default=False)
    owner = ForeignKeyField(Users, related_name='courses_owner', on_delete='CASCADE')
    group = ForeignKeyField(Groups, related_name='courses_group', on_delete='CASCADE')
    category = ForeignKeyField(Categories, related_name='courses_category', on_delete='CASCADE')
