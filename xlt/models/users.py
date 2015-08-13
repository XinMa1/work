# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.images import Images
from datetime import datetime

class Users(BaseModel):
    # 手机号码
    cellphone = CharField(unique=True)
    # 电子邮件地址
    email = CharField(unique=True)
    # 姓名(昵称)
    name = CharField(unique=True)
    # 密码
    password = CharField(unique=True)
    # 用户创建时间
    created_time = DateTimeField(default=datetime.now)
    # 最后登录时间
    last_login_time = DateTimeField(default=datetime.now)
    # 用户职位
    description = TextField(null=True)
    # 头像
    avatur = ForeignKeyField(Images, related_name='users_avatur', on_delete='CASCADE')
    # 性别
    gender = IntegerField()
    #用户微信
    weixin = CharField(unique=True)
    #用户地址
    address = TextField(null=True)
    #职位
    job = TextField(null=True)
