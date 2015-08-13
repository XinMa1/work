# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from datetime import datetime
from models.base import BaseModel
from models.images import Images

class Contacts(BaseModel):
    # 手机号码
    cellphone = CharField(unique=True)
    # 电子邮件地址
    email = CharField(unique=True)
    # 姓名(昵称)
    name = CharField(unique=True)
    # 用户创建时间
    created_time = DateTimeField(default=datetime.now)
    # 用户描述
    description = TextField(null=True)
    # 职位
    title = CharField(null=True)
    # 头像
    avatur = ForeignKeyField(Images, related_name='contacts_thumbnail', on_delete='CASCADE')
    # 性别
    gender = IntegerField(default=0)
    # 地址
    address = CharField(null=True)
    # 编号
    sn = CharField(unique=True)
    # 微信
    weixin = CharField(unique=True)
