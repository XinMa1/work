# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.users import Users
from models.courses import Courses
from models.transactions import Transactions
from datetime import datetime

class CoursePayments(BaseModel):
    course = ForeignKeyField(Courses, related_name='course_payments', on_delete='CASCADE')
    created_time = TimeField(formats="%Y-%m-%d %H:%M:%S",
            default=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    remark = TextField(null=True)
    transaction = ForeignKeyField(Transactions, related_name='course_payments_transaction', on_delete='CASCADE')
