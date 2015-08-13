# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.users import Users
from models.questions import Questions

class Albums(BaseModel):
    name = CharField(unique=True)
    description = TextField()
    thumbnail = TextField()
    owner = ForeignKeyField(Users, related_name='albums_owner', on_delete='CASCADE')
    question = ForeignKeyField(Questions, related_name='albums_question', on_delete='CASCADE')
