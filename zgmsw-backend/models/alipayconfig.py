# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from datetime import datetime

class Alipayconfig(BaseModel):
    partner = CharField(unique=True, max_length=16)
    key = CharField(unique=True, max_length=32)
    seller_email = CharField(unique=True, max_length=256)
