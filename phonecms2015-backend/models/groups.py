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
    # 详情介绍
    description = TextField(null=True)
    # 团队介绍
    team_description = TextField(null=True)
    # 缩略图
    thumbnail = ForeignKeyField(Images, related_name='groups_thumbnail', on_delete='CASCADE')
    # 创建者
    owner = ForeignKeyField(Users, related_name='groups_owner', on_delete='CASCADE')
    # 分类
    category = ForeignKeyField(Categories, related_name='groups_category', on_delete='CASCADE')
    # 区域
    regions = CharField(null=True)
    # 服务模式
    service_modes = TextField(null=True)
    # 特长
    specials = CharField(null=True)
    # 滚动图片相册
    swipeshow_album = ForeignKeyField(Albums, related_name='groups_swipeshow', on_delete='CASCADE')
    # 公司相册
    groups_album = ForeignKeyField(Albums, related_name='groups_album', on_delete='CASCADE')
    # 价格1: (标准价格)
    price1 = FloatField(default=0.0)
    # 价格2: (折扣价格)
    price2 = FloatField(default=0.0)
    # 位置: 经度
    longitude = FloatField(null=True)
    # 位置: 纬度
    latitude = FloatField(null=True)
    # 地址
    address = TextField(null=True)
    # 联系人
    contact = CharField(null=True)
    # 联系电话(座机)
    phoneno = CharField(null=True)
    # 联系电话(手机)
    cellphone = CharField(null=True)
    # 传真
    faxno = CharField(null=True)
    # 邮编
    postcode = CharField(null=True)
