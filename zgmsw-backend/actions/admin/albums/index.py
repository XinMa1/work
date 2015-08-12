# -*- coding: utf-8 -*-
#coding=utf-8

import web
from actions.admin.base import adminAction

'''
Admin controller: producing album administration views.
'''
class indexAction(adminAction):
    def __init__(self):
        adminAction.__init__(self)

    def GET(self):
        web.seeother(self.makeUrl('/admin/albums/list'))
