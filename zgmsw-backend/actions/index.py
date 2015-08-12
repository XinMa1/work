# -*- coding: utf-8 -*-
#coding=utf-8

from base import baseAction

'''
User controller: producing index views.
'''
class indexAction(baseAction):
    def __init__(self):
        baseAction.__init__(self)

    def GET(self):
        import web
        return web.redirect("/admin")
