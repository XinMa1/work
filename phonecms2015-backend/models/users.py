# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.roles import Roles
from datetime import datetime

class Users(BaseModel):
    # 手机号码
    cellphone = CharField(unique=True)
    # 电子邮件地址
    email = CharField(unique=True)
    # 姓名(昵称)
    name = CharField(unique=True)
    # 密码
    password = CharField()
    # 用户创建时间
    created_time = DateTimeField(default=datetime.now)
    # 最后登录时间
    last_login_time = DateTimeField(default=datetime.now)
    # 用户描述
    description = TextField()
    # 头像(base64 encoded)
    avatur = TextField()
    # 性别
    gender = IntegerField()
    # 角色
    role = ForeignKeyField(Roles, related_name='users')
    # 验证码
    verification_code = CharField(null=True)
    # 令牌
    token = TextField(unique=True, null=True)
    # 令牌生成时间
    token_created_time = DateTimeField(default=datetime.now)
