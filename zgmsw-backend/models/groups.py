# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.users import Users
from models.categories import Categories
from models.albums import Albums
from models.images import Images

class Groups(BaseModel):
    name = CharField(unique=True)
    # 班级详情
    description = TextField()
    # 教师团队
    teaching_team = TextField()
    # 班级缩略图
    thumbnail = ForeignKeyField(Images, related_name='groups_thumbnail', on_delete='CASCADE')
    # 所有人(班级管理员)
    owner = ForeignKeyField(Users, related_name='groups_owner', on_delete='CASCADE')
    # 学科种类
    category = ForeignKeyField(Categories, related_name='groups_category', on_delete='CASCADE')
    # 授课区域
    regions = CharField(null=True)
    # 授课方式
    teaching_modes = TextField(null=True)
    # 教学特长
    specials = CharField(null=True)
    # 滚动图片相册
    swipeshow_album = ForeignKeyField(Albums, related_name='groups_swipeshow', on_delete='CASCADE')
    # 班级相册
    groups_album = ForeignKeyField(Albums, related_name='groups_album', on_delete='CASCADE')
    # 老师上门价格
    price_home_service = CharField(null=True)
    # 学生上门价格
    price_remote_service = CharField(null=True)
    # 班级位置: 经度
    longitude = FloatField(null=True)
    # 班级位置: 纬度
    latitude = FloatField(null=True)
    # 班级聊天室id
    chatroom = CharField(null=True)
    # 班级聊天室名字
    chatroom_name = CharField(null=True)
    # 地址
    address = TextField(null=True)
    # 联系人
    contact = CharField(null=True)
    # 联系电话
    phoneno = CharField(null=True)
