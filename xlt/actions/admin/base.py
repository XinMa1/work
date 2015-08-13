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
class adminAction(htmlAction):
    def __init__(self, chkLogin=True, chkInstall=True):
        htmlAction.__init__(self)
        self.privData = {
            'GENDER_LIST':  { 1:'男', 0: '女'},
            'STATUS_LIST':  { 1:'已读', 0: '未读'},
            'TYPES_LIST':   { 1:'铝芯', 0: '铜芯'},
            'ACCOUNTINGS_STATUS':   { 2: '未同意',  1:'已审核', 0: '未审核'},
            'NAME':         config.NAME,
        }

        self.tmplDir = config.ADMIN_TMPLS_DIR
        self.render = web.template.render(self.tmplDir, globals=self.globalsTmplFuncs)
        self.privData['render'] = self.render
        
        if chkLogin and self.isLogin() != 'admin':
            raise web.seeother(self.makeUrl('/admin/login'))

        if chkInstall and not self.isInstalled():
            raise web.seeother(self.makeUrl('/admin/install'))

    def getPageStr(self, url, currentPage, perPageCount, totalCount=10000):
        totalPage = totalCount/perPageCount
        totalPage += 1 if totalCount%perPageCount else 0

        if '?' in url:
            url=url+'&page='
        else:
            url=url+'?page='

        pageString= ''

        if currentPage > 1:
            pageString += '''
                <span class="alignleft"><a href="'''+ url + str(currentPage-1)+'''"> &laquo;上页</a></span>
            '''
        if totalPage > currentPage:
            pageString += '''
            <span class="alignright"><a href="''' + url + str(currentPage+1)+'''"> 下页 &raquo;</a></span>
            '''
        return pageString

