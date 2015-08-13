# -*- coding: utf-8 -*-
#coding=utf-8

import web
import os
import config
from actions.admin.base import adminAction

'''
Admin controller: producing login views.
'''
class refererAction(adminAction):
    def __init__(self):
        adminAction.__init__(self, chkLogin=False, chkInstall=False)

    def GET(self, name):
        return self.notFound()
