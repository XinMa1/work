# -*- coding: utf-8 -*-
#coding=utf-8

from actions.admin.base import adminAction

'''
Admin controller: producing login views.
'''
class indexAction(adminAction):
    def __init__(self):
        adminAction.__init__(self, chkLogin=False, chkInstall=False)

    def index(self):
        return self.display('login')

    def GET(self):
        return self.index()

