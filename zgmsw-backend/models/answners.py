# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.users import Users
from models.questions import Questions
from datetime import datetime

class Answners(BaseModel):
    #回答类型，扩展作用
    type = CharField(default=1)
    # 回答开放1 关闭 0
    status = CharField(default=1)
    created_time = DateTimeField(default=datetime.now)
    content = TextField()
    owner = ForeignKeyField(Users, related_name='answners_owner', on_delete='CASCADE')
    question = ForeignKeyField(Questions,related_name='question_answners',on_delete='CASCADE')
