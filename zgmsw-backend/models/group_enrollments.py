# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.users import Users
from models.groups import Groups
from datetime import datetime

class GroupEnrollments(BaseModel):
    owner = ForeignKeyField(Users, related_name='group_enrollments_owner', on_delete='CASCADE')
    group = ForeignKeyField(Groups, related_name='enrollments', on_delete='CASCADE')
    created_time = DateTimeField(default=datetime.now)
