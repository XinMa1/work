# -*- coding: utf-8 -*-
#coding=utf-8

from action.weixin.base import wxAction
import hashlib
import web
import time
import config
from lxml import etree
import sys
from model.about import about
from model.info import info
from model.news import news
from model.product import product as modelProduct
from model.prodcomment import prodcomment as modelProdcomment
from log import log

'''
User controller: producing profile views.
'''
class actions(wxAction):
    def __init__(self, name = ''):
        wxAction.__init__(self, name)
        aboutObj = about().getOne('wxtoken', {})
        self.token = aboutObj['wxtoken']

    def GET(self):
        try:
            inputs = self.getInput()
            signature = inputs['signature']
            timestamp = inputs['timestamp']
            nonce = inputs['nonce']
            echostr=inputs['echostr']

            list=[self.token, timestamp, nonce]
            list.sort()
            sha1=hashlib.sha1()
            map(sha1.update,list)
            hashcode=sha1.hexdigest()

            if hashcode == signature:
                return echostr

            return self.notFound()
        except Exception, e:
            return self.notFound()
            

    def POST(self):
        try:
            str_xml = web.data() #获得post来的数据
            xml = etree.fromstring(str_xml) #进行XML解析
            msgType = xml.find("MsgType").text
            fromUser = xml.find("FromUserName").text
            toUser = xml.find("ToUserName").text

            if msgType == 'text':
                content = xml.find("Content").text #获得用户所输入的内容
                return self.handle_text_msg(fromUser, toUser, content)
            elif msgType == 'event':
                event = xml.find("Event").text
                eventType = xml.find("EventKey").text
                #log.info("handle event %s" % eventType)
                return self.handle_events(fromUser, toUser, eventType)
        except Exception, e:
            #log.warn(e)
            return self.notFound()


    def handle_events(self, fromUser, toUser, eventType):
        if eventType == 'news':
            return self.handle_event_news(fromUser, toUser)
        elif eventType == 'newprods': 
            return self.handle_event_new_prods(fromUser, toUser)
        elif eventType == 'hotprods': 
            return self.handle_event_hot_prods(fromUser, toUser)
        elif eventType == 'about': 
            return self.handle_event_about(fromUser, toUser)
        elif eventType == 'hornor': 
            return self.handle_event_hornor(fromUser, toUser)
        elif eventType == 'business': 
            return self.handle_event_business(fromUser, toUser)
        elif eventType == 'contact': 
            return self.handle_event_contact(fromUser, toUser)
        elif eventType == 'support': 
            return self.handle_event_support(fromUser, toUser)


    def handle_event_news(self, fromUser, toUser):
        try:
            newslist = news().getList("id, name, thumbnail",
                                 'category>1',
                                 orders="id desc",
                                 limits='5')
            for x in newslist:
                x['desc'] = ""
                x['url'] = "http://%s.wiaapp.cn/ajax/views/newscontent?id=%d" % (config.AJAX_TEMPLATE, x['id'])
                x['picurl']=self.imageUrl(x['thumbnail'])

            return self.render.wx_reply_list(fromUser, toUser,
                                            int(time.time()),
                                            len(newslist),
                                            newslist)
        except Exception, e:
            #log.warn(e)
            return self.notFound()


    def handle_event_new_prods(self, fromUser, toUser):
        try:
            items = modelProduct().getList('id,picture,name', 
                                           condition='category>1', 
                                           orders="id desc", 
                                           limits='5')
            for x in items:
                x['desc'] = ""
                x['url'] = "http://%s.wiaapp.cn/ajax/views/prodcontent?id=%d" % (config.AJAX_TEMPLATE, x['id'])
                x['picurl']=self.imageUrl(x['picture'])

            return self.render.wx_reply_list(fromUser, toUser,
                                            int(time.time()),
                                            len(items),
                                            items)
        except Exception, e:
            #log.warn(e)
            return self.notFound()

    def handle_event_hot_prods(self, fromUser, toUser):
        try:
            commentitems = modelProdcomment().getList('product,count(product)', '1=1 group by product', orders='count(product) desc',limits='5')
            products = []
            for item in commentitems:
                condition = 'id = ' + str(item['product'])
                prod = modelProduct().getOne('id,picture,name',condition)
                if (prod):
                    prod['desc'] = ""
                    prod['picurl'] = self.imageUrl(prod['picture'])
                    prod['url'] = "http://%s.wiaapp.cn/ajax/views/prodcontent?id=%d" % (config.AJAX_TEMPLATE, prod['id'])
                    products.append(prod)

            return self.render.wx_reply_list(fromUser, toUser,
                                            int(time.time()),
                                            len(products),
                                            products)

        except Exception, e:
            log.warn(e)
            return self.notFound()

    def handle_event_about(self, fromUser, toUser):
        try:
            res = info().getOne("id, thumbnail, content", {'id': config.WX_INFO_ID_ABOUT})
            return self.render.wx_reply_msg(fromUser, toUser, 
                                            int(time.time()), 
                                            title=u"企业介绍",
                                            desc=self.subText(self.htmlunquote(res['content']), 0, 64),
                                            picurl=self.imageUrl(res['thumbnail']),
                                            url="http://%s.wiaapp.cn/ajax/views/infocontent?id=%d" % (config.AJAX_TEMPLATE, config.WX_INFO_ID_ABOUT)
                                           )
        except Exception, e:
            #log.warn(e)
            return self.notFound()
            
    def handle_event_hornor(self, fromUser, toUser):
        try:
            res = info().getOne("id, thumbnail, content", {'id': config.WX_INFO_ID_HORNOR})
            return self.render.wx_reply_msg(fromUser, toUser, 
                                            int(time.time()), 
                                            title=u"企业荣誉",
                                            desc=self.subText(self.htmlunquote(res['content']), 0, 64),
                                            picurl=self.imageUrl(res['thumbnail']),
                                            url="http://%s.wiaapp.cn/ajax/views/infocontent?id=%d" % (config.AJAX_TEMPLATE, config.WX_INFO_ID_HORNOR)
                                           )
        except Exception, e:
            #log.warn(e)
            return self.notFound()

    def handle_event_business(self, fromUser, toUser):
        try:
            res = info().getOne("id, thumbnail, content", {'id': config.WX_INFO_ID_BUSINESS})
            return self.render.wx_reply_msg(fromUser, toUser,
                                            int(time.time()), 
                                            title=u"业务范围",
                                            desc=self.subText(self.htmlunquote(res['content']), 0, 64),
                                            picurl=self.imageUrl(res['thumbnail']),
                                            url="http://%s.wiaapp.cn/ajax/views/infocontent?id=%d" % (config.AJAX_TEMPLATE, config.WX_INFO_ID_BUSINESS)
                                           )
        except Exception, e:
            #log.warn(e)
            return self.notFound()

    def handle_event_contact(self, fromUser, toUser):
        try:
            res = info().getOne("id, thumbnail, content", {'id': config.WX_INFO_ID_CONTACT})
            return self.render.wx_reply_msg(fromUser, toUser, 
                                            int(time.time()), 
                                            title=u"联系我们",
                                            desc=self.subText(self.htmlunquote(res['content']), 0, 64),
                                            picurl=self.imageUrl(res['thumbnail']),
                                            url="http://%s.wiaapp.cn/ajax/views/infocontent?id=%d" % (config.AJAX_TEMPLATE, config.WX_INFO_ID_CONTACT)
                                           )
        except Exception, e:
            #log.warn(e)
            return self.notFound()

    def handle_event_support(self, fromUser, toUser):
        return self.render.wx_reply_msg(fromUser, toUser, 
                                        int(time.time()), 
                                        title=u"技术支持",
                                        desc=u"  武汉和网信息科技有限公司成立于2009年8月，是一家跨越传统互联网和移动互联网为广大中小企业提供全程电子商务服务的IT服务企业。\n\n  公司提供的产品和服务包括APP、WAP网站、WEB网站、网站的策划制作与运营、网站优化等，涵盖企业网站、行业信息门户、电子商务平台等项目，并为中小企业提供企业信息化培训与咨询服务。",
                                        picurl="http://www.whhe.cn/Templates/he2/html/images/index-logo-nav.jpg",
                                        url="http://whhe.wiaapp.cn/about/show"
                                       )

    def handle_text_msg(self, fromUser, toUser, content):
        return self.render.wx_reply_text(fromUser, toUser, int(time.time()), config.WX_DEFAULT_MSG)
