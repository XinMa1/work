# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel

class Version(BaseModel):
    description = TextField()
