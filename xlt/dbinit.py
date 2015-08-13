#!/usr/bin/env python
#coding=utf-8

from models.base import db
from models.version import Version
from models.categories import Categories
from models.products import Products
from models.images import Images
from models.orders import Orders
from models.order_details import OrderDetails
from models.users import Users
from models.contacts import Contacts
from models.news import News
from models.notifications import Notifications
from models.accountings import Accountings
from models.account_incommings import AccountIncommings
from models.account_outgoings import AccountOutgoings
from models.answers import Answers
from models.questions import Questions
from models.albums import Albums

import base64
from imaging import imaging

class dbinit(object):
    def __init__(self):
        db.connect()
        self.version = None
        self.admin = None
        self.sys_category = None
        self.default_thumbnail = None
        self.sys_image = None

        if not Version.table_exists():
            tables = [
                Version,
                Categories,
                Products,
                News,
                Notifications,
                Images,
                Orders,
                OrderDetails,
                Users,   
                Contacts,
                Accountings,
                AccountIncommings,
                AccountOutgoings,
                Questions,
                Answers,
                Albums
            ]
        
            db.create_tables(tables)

            self.version=Version.create(description=open('VERSION').read())
            self.default_thumbnail = base64.b64encode(buffer(imaging.default_thumbnail()))
  
 
            self.sys_category = Categories.create(
                            name = '系统预置分类',
                            description = '预置的初始父类!',
                         )

            self.sys_image = Images.create(
                            description = '预置的系统图片!',
                            thumbnail = self.default_thumbnail,
                            uuid = 'default'
                         )

            self.admin = Users.create(
                            name = 'admin',
                            cellphone = '13912345678',
                            email = 'admin@wiaapp.cn',
                            password = '21232f297a57a5a743894a0e4a801fc3',
                            gender = 0,
                            avatur = self.sys_image,
                            description = '系统管理员',
                            weixin= '0',
                            address= 'sv',
                         )

    def print_trace_log(self):
        if self.version:
            print 'Database Version: %s' % self.version.description

        if self.admin and self.sys_image:
            print 'Administrator: name=%s, cellphone=%s, email=%s' % (self.admin.name, 
                                                                  self.admin.cellphone, 
                                                                  self.admin.email)
            print 'Predefined System Image: uuid=%s, desc=%s' % (self.sys_image.uuid, 
                                                            self.sys_image.description)

if __name__ == '__main__':
    dbinit = dbinit()
    dbinit.print_trace_log()
