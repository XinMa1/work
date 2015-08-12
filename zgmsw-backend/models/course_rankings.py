# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.users import Users
from models.courses import Courses
from datetime import datetime

class CourseRankings(BaseModel):
    type = IntegerField()
    value = IntegerField(default=4)
    owner = ForeignKeyField(Users, related_name='course_rankings_owner', on_delete='CASCADE')
    course = ForeignKeyField(Courses, related_name='course_rankings', on_delete='CASCADE')
    created_time = DateTimeField(default=datetime.now)
