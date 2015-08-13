# -*- coding: utf-8 -*-
#coding=utf-8

import web
import os
import json
import config
from models.images import Images

import sys
reload(sys)
sys.setdefaultencoding('utf8')

'''
Basic controller
'''

class baseAction(object):
    def __init__(self):
        self.database = config.DATABASE
        self.globalsTmplFuncs = {
            'makeUrl'   : self.makeUrl,
            'imageUrl'  : self.imageUrl,
            'subStr'    : lambda strings,offset,length : self.subText(strings,offset,length),
            'str'       : lambda x : str(x)
        }

        self.tmplDir = None
        self.render = None

    def makeUrl(self, url, params={}):
        import urllib
        paramsStr = '?'+ urllib.urlencode(params) if len(params)>0 else ''
        return url + paramsStr

    def imageUrl(self, uuid):
        return config.UPLOAD_URL + '/image/%s.jpeg' % uuid 

    def isInstalled(self):
        try:
            from models.version import Version
            return True if Version.table_exists() else False
        except Exception, e:
            return False

    def isLogin(self):
        if not hasattr(web.ctx.session, 'login'):
            return None

        if not web.ctx.session.login:
            return None

        if not hasattr(web.ctx.session, 'username'):
            return None

        return web.ctx.session.username

    def isAdmin(self):
        return self.isLogin() == 'admin'

    def setLogin(self, username = None):
        if username == None:
            web.ctx.session.login = False
            web.ctx.session.username = None
        else:
            web.ctx.session.login = True
            web.ctx.session.username = username

    def validates(self, validList):
        userInput=self.getInput()
        for i in validList:
            if not i.validate(userInput[i.name]):
                self.errorMessage=i.note
                return False
        return True

    def subText(self, strings, offset, length):
        try:
            decoded = self.strip_tags(strings).decode('utf-8').lstrip()
            encoded = decoded[offset:length].encode('utf-8')
            if len(decoded) > length:
                encoded += "..."

            return encoded
        except Exception, e:
            return '...'

    def strip_tags(self, html):
        if not html:
            return ""

        from HTMLParser import HTMLParser
        html=html.strip()
        html=html.strip("\n")
        result=[]
        parse=HTMLParser()
        parse.handle_data=result.append
        parse.feed(html)
        parse.close()
        return "".join(result)

    def getInput(self):
        return self.htmlquote(dict(web.input()))

    def htmlquote(self,inputData):
        if isinstance(inputData,dict) == False:
            return web.net.htmlquote(inputData)
        else:
            for k,v in inputData.items():
                inputData[k]= self.htmlquote(v)
        return inputData
  
    def htmlunquote(self,inputData):
        if isinstance(inputData,dict) == False:
            return web.net.htmlunquote(inputData)
        else:
            for k,v in inputData.items():
                inputData[k]= self.htmlunquote(v)
        return inputData

    def htmlunescape(self,inputData):
        try:
            import htmllib
            p = htmllib.HTMLParser(None)
            p.save_bgn()
            p.feed(inputData)
            return p.save_end()
        except Exception, e:
            return inputData

    def display(self, tmpl):
        if not self.render:
            return web.nomethod()

        return getattr(self.render, tmpl)(self.privData)

class htmlAction(baseAction):
    def __init__(self):
        baseAction.__init__(self)

    def success(self, msg, url='/', timeout=5):
        self.privData['JUMP_MSG'] = msg
        self.privData['JUMP_TIMEOUT'] = timeout
        self.privData['JUMP_URL'] = url

        return self.display('success')


    def error(self, msg, url='/', timeout=5):
        self.privData['JUMP_MSG'] = msg
        self.privData['JUMP_TIMEOUT'] = timeout
        self.privData['JUMP_URL'] = url

        return self.display('error')

    def back(self, msg, timeout=5):
        self.privData['JUMP_MSG'] = msg
        self.privData['JUMP_TIMEOUT'] = timeout

        return self.display('back')

    def notFound(self):
        return self.error(msg='Page not found!')

class jsonAction(baseAction):
    def __init__(self):
        baseAction.__init__(self)

    def success(self, msg = ''):
        return web.ok()

    def error(self):
        return web.BadRequest()

    def unauthorized(self):
        return web.Unauthorized()

    def forbidden(self):
        return web.Forbidden()

    def notFound(self):
        return web.NotFound()
