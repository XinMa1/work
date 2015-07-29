# -*- coding: utf-8 -*-
#coding=utf-8

from actions.admin.base import adminAction
from models.albums import Albums

class indexAction(adminAction):
    def __init__(self):
        adminAction.__init__(self)

    def GET(self):
        return self.index()

    def index(self):
        condition = {}
        albumsList = albums().getList('*', condition)
        
        self.privData['ALBUMS_LIST'] = {}
        for item in albumsList:
            self.privData['ALBUMS_LIST'][item['id']] = item['name']

        return self.display('upload')

