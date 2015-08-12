# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.users import Users
from models.groups import Groups
from datetime import datetime

class GroupFavorites(BaseModel):
    owner = ForeignKeyField(Users, related_name='group_favorites_owner', on_delete='CASCADE')
    group = ForeignKeyField(Groups, related_name='group_favorites', on_delete='CASCADE')
    created_time = DateTimeField(default=datetime.now)
