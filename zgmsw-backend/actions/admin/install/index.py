# -*- coding: utf-8 -*-
#coding=utf-8

import web
from actions.admin.base import adminAction

'''
User controller: producing install views.
'''
class indexAction(adminAction):
    def __init__(self):
        adminAction.__init__(self, chkInstall=False)

    def index(self):
        return self.display('install')

    def GET(self):
        return self.index()
