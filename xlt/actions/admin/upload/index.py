# -*- coding: utf-8 -*-
#coding=utf-8

from actions.admin.base import adminAction

class indexAction(adminAction):
    def __init__(self):
        adminAction.__init__(self)

    def GET(self):
        return self.index()

    def index(self):
        return self.display('upload')

