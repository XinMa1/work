#!/usr/bin/env python
#coding=utf-8

from models.base import db
from models.version import Version
from models.albums import Albums
from models.categories import Categories
from models.product_comments import ProductComments
from models.product_favorites import ProductFavorites
from models.product_rankings import ProductRankings
from models.product_payments import ProductPayments
from models.products import Products
from models.group_payments import GroupPayments
from models.group_comments import GroupComments
from models.group_favorites import GroupFavorites
from models.group_rankings import GroupRankings
from models.groups import Groups
from models.images import Images
from models.roles import Roles
from models.transactions import Transactions
from models.users import Users
from models.articles import Articles
from models.answners import Answners
from models.questions import Questions
from models.chatrooms import Chatrooms

import base64
from imaging import imaging

class dbinit(object):
    def __init__(self):
        db.connect()
        if not Version.table_exists():
           
            tablesName = [
                Version,
                Albums,
                Chatrooms,
                Categories,
                ProductComments,
                ProductFavorites, 
                ProductRankings,
                ProductPayments,
                Products,
                GroupComments,
                GroupFavorites, 
                GroupRankings,
                GroupPayments,
                Groups,
                Images,
                Roles,
                Transactions,
                Users,   
                Articles,
                Answners,
                Questions, 
            ]
        
            for i in tablesName:
                i.create_table()


        self.version=Version.get_or_create(description=open('VERSION').read())
        self.admin_role = Roles.get_or_create(type=1,  description='系统管理员')
        self.assistant_role = Roles.get_or_create(type=10, description='班级管理员')
        self.student_role = Roles.get_or_create(type=100,  description='注册学员')
        self.default_thumbnail = base64.b64encode(buffer(imaging.default_thumbnail()))
  
 
        self.sys_categories = Categories.get_or_create(
                            name = '系统预置分类',
                            description = '预置的初始父类!',
                            thumbnail = self.default_thumbnail,
                         )


        self.admin = Users.get_or_create(
                            name = 'admin',
                            cellphone = '13912345678',
                            email = 'admin@wiaapp.cn',
                            password = '21232f297a57a5a743894a0e4a801fc3',
                            gender = 0,
                            role = self.admin_role,
                            description = '预置的系统管理员!',
                            avatur = self.default_thumbnail
                     )

        self.sys_album = Albums.get_or_create(
                            name = '系统专辑',
                            description = '预置的系统专辑!',
                            thumbnail = self.default_thumbnail,
                            owner = self.admin
                         )

        self.sys_image = Images.get_or_create(
                            description = '预置的系统图片!',
                            thumbnail = self.default_thumbnail,
                            owner = self.admin,
                            album = self.sys_album,
                            uuid = 'default'
                         )


    def print_trace_log(self):
        print 'Database Version: %s' % self.version.description
        print 'Role Admin: type=%d, desc=%s' % (self.admin_role.type, self.admin_role.description)
        print 'Role Assistant: type=%d, desc=%s' % (self.assistant_role.type, self.assistant_role.description)
        print 'Role Student: type=%d, desc=%s' % (self.student_role.type, self.student_role.description)
        print 
        print 'Administrator: name=%s, cellphone=%s, email=%s' % (self.admin.name, 
                                                                  self.admin.cellphone, 
                                                                  self.admin.email)
        print 'Predefined System Album: name=%s, desc=%s' % (self.sys_album.name, self.sys_album.description)
        print 'Predefined System Image: uuid=%s, desc=%s' % (self.sys_image.uuid, self.sys_image.description)

if __name__ == '__main__':
    dbinit = dbinit()
    dbinit.print_trace_log()
