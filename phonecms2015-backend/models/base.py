# -*- coding: utf-8 -*-
#!/usr/bin/env python
#coding=utf-8

import config
from peewee import *

class SqliteFKDatabase(SqliteDatabase):
    def initialize_connection(self, conn):
        self.execute_sql('PRAGMA foreign_keys=ON;')

db = SqliteFKDatabase(config.DATABASE)

class BaseModel(Model):
    class Meta:
        database = db

