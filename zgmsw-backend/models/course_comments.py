# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.users import Users
from models.courses import Courses
from datetime import datetime

class CourseComments(BaseModel):
    owner = ForeignKeyField(Users, related_name='course_comments_owner', on_delete='CASCADE')
    course = ForeignKeyField(Courses, related_name='course_comments', on_delete='CASCADE')
    created_time = DateTimeField(default=datetime.now)
    content = TextField(null=True)
    value = IntegerField(default=4)
