# -*- coding: utf-8 -*-
#coding=utf-8

import web
from action.admin.base import adminAction

'''
Admin controller: producing album administration views.
'''
class indexAction(adminAction):
    def __init__(self, name = '微信管理'):
        adminAction.__init__(self, name)

    def GET(self):
        web.seeother(self.makeUrl('/admin/weixin/list'))
