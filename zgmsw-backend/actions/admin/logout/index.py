# -*- coding: utf-8 -*-
#coding=utf-8


from actions.admin.base import adminAction

'''
Admin controller: producing admin logout.
'''
class indexAction(adminAction):
    def __init__(self):
        adminAction.__init__(self)

    def index(self):
        self.setLogin()
        return self.success('已退出系统', url='/admin/login')

        
    def GET(self):
        return self.index()        
