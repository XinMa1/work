# -*- coding: utf-8 -*-
#coding=utf-8

import os
import web
import config
from action.base import jsonAction

'''
Weixin base controller
'''
class wxAction(jsonAction):
    def __init__(self, name='wxAction'):
        jsonAction.__init__(self, name)
        self.name = name
        self.tmplDir = os.path.join(config.TMPL_DIR, 'weixin', config.WEIXIN_TEMPLATE)
        self.render = web.template.render(self.tmplDir, globals=self.globalsTmplFuncs)
        self.privData['render'] = self.render
