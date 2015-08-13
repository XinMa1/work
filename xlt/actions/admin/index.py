# -*- coding: utf-8 -*-
#coding=utf-8

import web
import os
import config
from log import log

from base import adminAction

'''
Admin controller: producing admin views.
'''
class indexAction(adminAction):
    def __init__(self):
        adminAction.__init__(self)

    def index(self):
        import time
        self.privData['CLIENT_IP'] = web.ctx.ip
        self.privData['DATE'] = str(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        self.privData['USER_AGENT'] = web.ctx.environ['HTTP_USER_AGENT']
        self.privData['SERVER_IP'] = web.ctx.environ['REMOTE_ADDR']
        
        return self.display('index')

        
    def GET(self):
        return self.index()
        
