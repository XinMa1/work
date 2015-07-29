# -*- coding: utf-8 -*-
#!/usr/bin/env python

from peewee import *
from models.base import BaseModel
from models.users import Users
from models.categories import Categories
from models.groups import Groups
from models.images import Images
from models.albums import Albums
from datetime import datetime

class Products(BaseModel):
    # 视频名称
    video_name = TextField(null = True)
    # 视频描述
    video_desc = TextField(null = True)
    # 视频web播放链接
    video_url = TextField(null = True)
    # 视频mobile播放链接
    video_mobile_url = TextField(null=True)
    video_adaptive_url = TextField(null=True)
    # 视频码率
    video_rate = TextField(null=True)
    # 视频宽度
    video_width =  IntegerField(null=True)
    # 视频高度
    video_height = IntegerField(null=True)
    # 视频缩略图
    video_thumbnail = TextField(null=True)
    video_uptime = TextField(null=True)
    # 视频播放时长
    video_duration = TextField(null=True)
    # 产品创建时间
    created_time = DateTimeField(default=datetime.now)
    # 产品名称
    name = CharField(unique=True)
    # 产品价格
    price = FloatField(default=.0)
    # 产品折扣价格
    discount = FloatField(default=.0)
    # 产品描述
    description = TextField(null=True)
    # 产品缩略图
    thumbnail = ForeignKeyField(Images, related_name='products_thumbnail')
    # 产品所有者
    owner = ForeignKeyField(Users, related_name='products_owner', on_delete='CASCADE')
    # 所属公司
    group = ForeignKeyField(Groups, related_name='products_group', on_delete='CASCADE')
    # 所属分类
    category = ForeignKeyField(Categories, related_name='products_category', on_delete='CASCADE')
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
    # 相册
    products_album = ForeignKeyField(Albums, related_name='products_album', on_delete='CASCADE')
    # 区域
    regions = CharField(null=True)
    # 服务模式
    service_modes = TextField(null=True)
    # 特长
    specials = CharField(null=True)
    # 滚动图片相册
    swipeshow_album = ForeignKeyField(Albums, related_name='products_swipeshow', on_delete='CASCADE')
 
    # 团队介绍
    team_description = TextField()
