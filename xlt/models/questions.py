# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.users import Users
from datetime import datetime
import time
ISOTIMEFORMAT='%Y-%m-%d'
class Questions(BaseModel):
    title = CharField(default='')
    #问题类型，扩展作用
    # 问题开放1 关闭 0
    status = CharField(default=1)
    created_time = DateField(default=time.strftime(ISOTIMEFORMAT,time.localtime(time.time())))
    content = TextField(default='')
    uuid1=CharField()
    img1= TextField()
    uuid2=CharField()
    img2= TextField()
    uuid3=CharField()
    img3= TextField()
    owner = ForeignKeyField(Users, related_name='questions_owner', on_delete='CASCADE')
