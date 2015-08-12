# -*- coding: utf-8 -*-
#coding=utf-8

import config
from action.admin.base import adminAction
from model.about import about
import urllib2
import json

'''
Admin controller: producing weixin administration views.
'''
class refererAction(adminAction):
    def __init__(self, name = '微信管理'):
        adminAction.__init__(self, name)

        aboutObj = about().getOne('wxtoken,wxappid,wxsecret', {})
        self.appid = aboutObj['wxappid']
        self.secret = aboutObj['wxsecret']
        self.url_access_token = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (self.appid, self.secret)

    def GET(self, name):
        if name == 'list':
            return self.list()
        elif name == 'menuAdd':
            return self.menuAdd()
        elif name == 'menuDel':
            return self.menuDel()

        return self.notFound()

    def list(self):
        return self.display('wxList')

    def gen_access_token(self):
        # weixin access token remains vaild within 7200 secs.
        return json.loads(urllib2.urlopen(self.url_access_token).read())["access_token"]

    def menuAdd(self):
        menu = '''{
        "button":[
        {
           "name":"企业动态",
           "sub_button":[
            {
               "type":"click",
               "name":"最新新闻",
               "key":"news"
            },
            {
               "type":"view",
               "name":"3G网站",
               "url":"%s"
            }]
         },

         {
           "name":"企业产品",
           "sub_button":[
            {
               "type":"click",
               "name":"最新产品",
               "key":"newprods"
            },
            {
               "type":"click",
               "name":"最热产品",
               "key":"hotprods"
            }]
         },

         {
           "name":"关于我们",
           "sub_button":[
            {
               "type":"click",
               "name":"企业介绍",
               "key":"about"
            },
            {
               "type":"click",
               "name":"企业荣誉",
               "key":"hornor"
            },
            {
               "type":"click",
               "name":"业务范围",
               "key":"business"
            },
            {
               "type":"click",
               "name":"联系我们",
               "key":"contact"
            },
            {
                "type":"click",
                "name":"技术支持",
                "key":"support"
            }]
          }]
        }''' % (config.WEB_URL)

        try:
            url_menu_create = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=" + self.gen_access_token()
            res = json.loads(urllib2.urlopen(url_menu_create, menu.encode('utf-8')).read())
            if res['errcode'] == 0:
                return self.success(msg='创建微信菜单成功', url=self.makeUrl('/admin/weixin'))
            else:
                return self.error(msg='创建微信菜单失败: %s' % res['errmsg'], url=self.makeUrl('/admin/weixin'))
        except Exception, e:
            return self.error(msg='创建微信菜单失败: %s' % e, url=self.makeUrl('/admin/weixin'))

    def menuDel(self):
        #try:
        url_menu_delete = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=" + self.gen_access_token()
        res = json.loads(urllib2.urlopen(url_menu_delete).read())
        if res['errcode'] == 0:
            return self.success(msg='删除微信菜单成功', url=self.makeUrl('/admin/weixin'))
        else:
            return self.error(msg='删除微信菜单失败: %s' % res['errmsg'], url=self.makeUrl('/admin/weixin'))
        #except Exception, e:
        #    return self.error(msg='删除微信菜单失败: %s' % e, url=self.makeUrl('/admin/weixin'))
