# -*- coding: utf-8 -*-
#coding=utf-8

import web
import os
import config
from log import log
from actions.base import htmlAction


'''
Admin controller: used for producing views for desktop clients.
'''
class wapAction(htmlAction):
    def __init__(self):
        htmlAction.__init__(self)
        self.privData = {
            'GENDER_LIST':  { 1:'男', 0: '女'},
            'STATUS_LIST':  { 1:'已读', 0: '未读'},
            'TYPES_LIST':   { 1:'铝芯', 0: '铜芯'},
            'ACCOUNTINGS_STATUS':   { 2: '未同意', 1:'已审核', 0: '未审核'},
            'NAME':         config.NAME,
        }

        self.tmplDir = config.WAP_TMPLS_DIR
        self.render = web.template.render(self.tmplDir, globals=self.globalsTmplFuncs)
        self.privData['render'] = self.render
        
    def success(self, msg, url='/wap/home', timeout=5):
        return htmlAction.success(self, msg, url, timeout)

    def error(self, msg, url='/wap/home', timeout=5):
        return htmlAction.error(self, msg, url, timeout)
