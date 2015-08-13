# -*- coding: utf-8 -*-
#coding=utf-8

from base import wapAction
from config import COUNT_PER_PAGE
from models.images import Images
from models.categories import Categories
from models.users import Users
from models.contacts import Contacts
from models.news import News
from models.products import Products
from models.notifications import Notifications
from models.orders import Orders
from models.order_details import OrderDetails
from models.accountings import Accountings
from models.account_incommings import AccountIncommings
from models.account_outgoings import AccountOutgoings
from models.questions import Questions
from models.answers import Answers
from models.albums import Albums
from models.images import Images

import peewee
import utils
import web
import sys
import hashlib
import time
from datetime import datetime
from uploadmgr import httpUploadedFile
import string
import config
import os
import base64
from imaging import imaging
import cgi
#from model.about import about
import urllib2
import json
import random as rand

'''
Wap Actions Weixin签名管理
'''
class wxSign:
    def __init__(self, jsapi_ticket, pageurl):
        self.ret = {
            'nonceStr': self.__create_nonce_str(),
            'jsapi_ticket': jsapi_ticket,
            'timestamp': self.__create_timestamp(),
            'url': pageurl
        }
        #print 'nonceStr-',self.ret['nonceStr']
        #print 'jsapi_ticket-',self.ret['jsapi_ticket']
        #print 'timestamp-',self.ret['timestamp']
        #print 'url-',self.ret['url']


    def __create_nonce_str(self):
        return ''.join(rand.choice(string.ascii_letters + string.digits) for _ in range(15))

    def __create_timestamp(self):
        return int(time.time())

    def sign(self):
        string1 = '&'.join(['%s=%s' % (key.lower(), self.ret[key]) for key in sorted(self.ret)])
        #print 'sting1-',string1
        self.ret['signature'] = "'"+hashlib.sha1(string1).hexdigest()+"'"
        self.ret['nonceStr']="'"+self.ret['nonceStr']+"'"
        #print 'signature-',self.ret['signature']
        return self.ret

class wxTicket():
    def __init__(self):
        #aboutObj = about().getOne('wxtoken,wxappid,wxsecret', {})
        self.appid = 'wxbf04da4daf7549b8'#aboutObj['wxappid']
        self.secret = '4916077208c0bcf092e279856f4dd144'#aboutObj['wxsecret']
        self.url_access_token = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s" % (self.appid, self.secret)
        self.this_page_url='http://xlt.wiaapp.cn/wap/add_question'

    def get_access_token(self):
        '''
        @获取access_token
        '''
        # weixin access token remains vaild within 7200 secs.
        self.access_token = json.loads(urllib2.urlopen(self.url_access_token).read())["access_token"]
        self.url_jsapi_ticket='https://api.weixin.qq.com/cgi-bin/ticket/getticket?access_token=%s&type=jsapi'%self.access_token
        self.jsapi_ticket=json.loads(urllib2.urlopen(self.url_jsapi_ticket).read())["ticket"]
        #print 'jsapi_ticket-',self.jsapi_ticket

    def get_signature(self):
        try:
            self.get_access_token()
            wxSingTicket=wxSign(self.jsapi_ticket,self.this_page_url)
            self.result=wxSingTicket.sign()
            return self.result
        except Exception, e:
            print e
            return ''
'''
Wap Actions
'''
class refererAction(wapAction):
    def __init__(self):
        wapAction.__init__(self)

    def GET(self, name):
        if name == 'login':
            return self.login()

        current_user = self.isLogin()
        if not current_user or current_user == 'admin':
            raise web.seeother(self.makeUrl('/wap/login'))

        if name == 'home':
            return self.home()
        elif name == 'logout':
            return self.logout()
        elif name == 'categories':
            return self.categories()
        elif name == 'edit_my_information':
            return self.edit_my_information()
        elif name == 'edit_price_sheet':
            return self.edit_price_sheet()
        elif name == 'intro':
            return self.intro()
        elif name == 'contacts_list':
            return self.contacts_list()
        elif name == 'news_list':
            return self.news_list()
        elif name == 'news_details':
            return self.news_details()
        elif name == 'product_prices':
            return self.product_prices()
        elif name == 'notifications_list':
            return self.notifications_list()
        elif name == 'notification_details':
            return self.notification_details()
        elif name == 'orders_list':
            return self.orders_list()
        elif name == 'prices_list':
            return self.prices_list()
        elif name == 'contact_details':
            return self.contact_details()
        elif name == 'about_us':
            return self.about_us()
        elif name == 'honors':
            return self.honors()
        elif name == 'contact_us':
            return self.contact_us()
        elif name == 'my_information':
            return self.my_information()
        elif name == 'accountings_list':
            return self.accountings_list()
        elif name == 'accounting_details':
            return self.accounting_details()
        elif name == 'price_sheet_details':
            return self.price_sheet_details()
        elif name == 'export_price_sheet':
            return self.export_price_sheet()
        elif name == 'delete_price_sheet':
            return self.delete_price_sheet()
        elif name == 'add_price_sheet':
            return self.add_price_sheet()
        elif name == 'questions':
            return self.questions()
        elif name == 'question_details':
            return self.question_details()
        elif name == 'question_imglst':
            return self.question_imglst()
        elif name == 'delete_order_details':
            return self.delete_order_details()
        elif name == 'add_question':
            return self.add_question()
        
        return self.notFound()
    
    def POST(self, name):
        cgi.maxlen = int(config.MAX_UPLOAD_FILE_SIZE) * 1024 * 1024 # 2MB
        try:
            i = web.input(file={})
        except ValueError:
            return self.error(msg = '文件最大尺寸不能超过2M!')
        
        if name == 'signin':
            return self.signin()

        current_user = self.isLogin()
        if not current_user or current_user == 'admin':
            raise web.seeother(self.makeUrl('/wap/login'))

        if name == 'signout':
            return self.signout() 
        elif name == 'select_order':
            return self.select_order()
        elif name =='confirm_accountings':
            return self.confirm_accountings()
        elif name == 'save_my_information':
            return self.save_my_information()
        elif name == 'save_price_sheet':
            return self.save_price_sheet()
        elif name =='confirm_select_order':
            return self.confirm_select_order()
        elif name == 'logout':
            return self.logout()
        elif name == 'answer_question':
            return self.answer_question()
        elif name == 'raise_question':
            return self.raise_question()

        return self.notFound()
        
    def login(self):
        return self.display('login')
    def logout(self):
        web.ctx.session.login = False
        web.ctx.session.username = None        
        return self.login()    
    
    def save_my_information(self):
        inputs = web.input()
        try:
            try:
                if len(inputs['imgfile'])>10:
                    htmlimg = httpUploadedFile(inputs['imgfile'])
                    userimg=Images().create(
                        uuid =  htmlimg.uuid(),
                        description = self.htmlunquote("上传图片"),
                        thumbnail = self.wap_imgsave(htmlimg)
                        )
            except Exception, e:
                print e
                userimg=Images().get(Images.id == 1)
            
            user = Users.get(Users.id == int(inputs['userid']))
            user.name = inputs['name']
            user.cellphone = inputs['cellphone']
            user.gender = inputs['gender']
            user.email = inputs['email']
            user.job = inputs['job']
            user.avatur=userimg
            user.address = inputs['address']
            user.save()
            return self.my_information()
        except Exception, e:
            print e
            return self.error(msg='保存用户信息失败!')

    def answer_question(self):
        inputs = self.getInput()
        try:
            #import pdb;pdb.set_trace()
            content = inputs['content']
            user = Users.get(Users.name == self.isLogin())
            answer = Answers.create(
               owner = user,
               content = content,
               question = inputs['id'],
            )
            answer.save()
            return web.seeother(self.makeUrl('/wap/question_details', {'id':inputs['id']}))
        except Exception,e:
            print e
            return self.error(msg='回复问题失败！')        
      
    def questions(self):
        try:
            #import pdb;pdb.set_trace()
            questionList = Questions.select().order_by(Questions.id.desc())
            Listtemp=[]
            for item in questionList:
                length = Answers.select().where(item.id ==Answers.question).count()
                Listtemp.append([item,length])
            self.privData['QUESTIONS_LIST'] = Listtemp
            return self.display('questions-list')
        except Exception,e:
            print e
            return self.error(msg='获取问题列表信息失败!')
 
    def question_details(self):
        inputs = self.getInput()
        try:
            #import pdb;pdb.set_trace()
            question = Questions.get(Questions.id == inputs['id'])
            self.privData['QUESTION_DETAIL'] =question
            albumList = Albums.select().where(Albums.question ==inputs['id'])
            self.privData['ALUBUM'] =albumList
            answersList=Answers.select().where(Answers.question ==inputs['id'])
            self.privData['ANSWERS_LIST'] =answersList
            return self.display('question-details')
        except Exception, e:
            return self.error(msg='获取问题详情失败！')

    def question_imglst(self):
        inputs = self.getInput()
        try:
            #import pdb;pdb.set_trace()
            self.privData['IMG'] ='../../static/uploads/image/'+inputs['id']+'.jpeg'
            return self.display('original-image')
        except Exception, e:
            print e
            return self.error(msg='获取问题详情失败！')
        
    def wap_imgsave(self,imgfile):
        im = imaging(imgfile.target())
        try: 
            iw = int(im.size()[0])
            ih = int(im.size()[1])
        except Exception, e:
            iw = config.IMAGE_XRES
            ih = config.IMAGE_YRES
            
        tmpfile = imgfile.target() + ".tmp"
        data = im.resize(iw, ih) 
        file(tmpfile, 'w').write(data)
        os.unlink(imgfile.target())
        os.rename(tmpfile, imgfile.target())

        
        tw = config.THUMBNAIL_XRES
        th = config.THUMBNAIL_YRES

        blob = im.resize(tw, th)
        imgthumbnail = base64.b64encode(buffer(blob))
        
        return imgthumbnail

    def raise_question(self):
        inputs = web.input()
        user =Users.get(Users.name == self.isLogin())
        self.desc = '提问上传图片'
        self.ref = ''
        try:
            title = inputs['title']
            content =inputs['content']
            imgfilelst=[]
            imageslst=[]
            imgfilelst.append(inputs['imgfile1'])
            imgfilelst.append(inputs['imgfile2'])
            imgfilelst.append(inputs['imgfile3'])
            for item in imgfilelst:
                try:
                    if len(item)>10:
                        htmlimg = httpUploadedFile(item)
                        imageslst.append([htmlimg.uuid(),self.wap_imgsave(htmlimg)])
                    else:
                        imageslst.append(["default",Images().get(Images.id == 1).thumbnail])
                except Exception, e:
                    imageslst.append(["default",Images().get(Images.id == 1).thumbnail])
            
            self.privData['USER'] = user
            question = Questions.create(
                title = title,
                content = content,
                owner = user,
                uuid1=imageslst[0][0],
                uuid2=imageslst[1][0],
                uuid3=imageslst[2][0],
                img1=imageslst[0][1],
                img2=imageslst[1][1],
                img3=imageslst[2][1]
                
            )
            question.save()
            return self.questions()
        except Exception, e:
            print e
            return self.error(msg='提交问题失败!')

    def add_question(self):
        user =Users.get(Users.name == self.isLogin())
        imagesList = Images().select()

        # 确认当前用户是否至少有一个包含图片的专辑
        if not imagesList.count():
            return self.error(msg = '请创建至少一个图片!', url=self.makeUrl('/admin/images/list'))
        self.privData['IMAGES_LIST'] = imagesList
        self.privData['CURRENT_IMG'] = imagesList[0]
        self.privData['SUBMIT_NAME'] = "thumbnail"
        
        try:
            #import pdb;pdb.set_trace()
            self.privData['USER'] = user
            return self.display('raise-question')
        except Exception, e:
            print e
            return self.error(msg='页面跳转失败!')
     
    def delete_price_sheet(self):
        inputs = self.getInput()
        try:
            order = Orders.get(Orders.id == int(inputs['id']))
            order.delete_instance()
            return self.orders_list()
        except Exceptions, e:
            return self.error(msg='删除订单失败!')

    def delete_order_details(self):
        inputs = self.getInput()
        try:
            details = OrderDetails.get(OrderDetails.id == int(inputs['id']))
            details.delete_instance()
            return web.seeother(self.makeUrl('/wap/edit_price_sheet', {'id': details.order.id}))
        except Exceptions, e:
            return self.error(msg='删除订单失败!')

                    
    def confirm_select_order(self):
        inputs = self.getInput()
        try:
            product = Products.get(Products.id == int(inputs['product']))
            user =Users.get(Users.name == self.isLogin())
            price = inputs['price']
            if inputs.has_key('add'):
                order = Orders.create(
                    owner = user,
                    price = price,
                    description = product.category.name,
                )
            else:
                if not inputs.has_key('selected'):
                    return self.orders_list()
                order = Orders.get(Orders.id == int(inputs['selected']))
            
            details = OrderDetails.create(
                name = product.category.name + "   "+product.diameter,
                product = product,
                count = user,
                price = price,
                ratio = 0.0,
                order = order,
            )
            return web.seeother(self.makeUrl('/wap/edit_price_sheet', {'id': order.id}))
        except Exception, e:
            print 'exc',e
            return self.error(msg='保存订单失败!')

    def add_price_sheet(self):
        try:
            user =Users.get(Users.name == self.isLogin())
            order = Orders.create(
                owner = user,
                price = 0.0,
                description = '新报价单',
            )
            return web.seeother(self.makeUrl('/wap/edit_price_sheet', {'id': order.id}))
            #return self.orders_list()
        except Exception, e:
            return self.error(msg='保存订单失败!')
                           
    def save_price_sheet(self):
        inputs = self.getInput()
        print inputs
        try:
            if inputs.has_key('add'):
                return web.seeother(self.makeUrl('/wap/categories', {'parent': 1, 'order': int(inputs['id'])}))

            order = Orders.get(Orders.id == int(inputs['id']))

            attrs = {}
            for k, v in inputs.items():
                try:
                    attr, oid = k.split('_')
                except Exception, e:
                    continue

                if not attrs.has_key(oid):
                    attrs[oid] = {}
                attrs[oid][attr] = v

            if not inputs['customer'] or not inputs['description']:
                raise Exception("询价方或备注不能为空!")

            order.customer = inputs['customer']
            order.description = inputs['description']
            order.owner = Users.get(Users.name == self.isLogin())
            order.save()

            for k, v in attrs.items():
                #import pdb;pdb.set_trace()
                import traceback
                if not v['count'] or not v['ratio']:
                    raise Exception("数量或利润率不能为空!")
                nameform = v['name']
                diameterform = v['diameter']
                oldinput= v['can']
                name, diameter = oldinput.split('   ')
                details = OrderDetails.get(OrderDetails.id == int(k))
                details.name = oldinput
                flag = v['bool']
                if flag.find("True")>=0:
                   details.flag=True
                elif details.name!=(details.product.category.name+'   '+details.product.diameter):
                   details.flag=True
                else:                   
                   details.flag=False
                   
                try:
                    product = Products().get(Products.name==name,Products.diameter == diameter)
                except Exception,e:
                    details.price = float(v['input'])
                    details.count = v['count']
                    details.ratio = float(v['ratio'])/100.0
                    details.save()
                  
                details.price = float(v['input'])
                details.count = v['count']
                details.ratio = float(v['ratio'])/100.0
                details.save()
                
            return web.seeother(self.makeUrl('/wap/price_sheet_details', {'id': order.id}))
        except Exception, e:
            print e
            return self.error(msg='保存报价单信息失败: %s' % e)

    def home(self):
        self.notifications_list()
        return self.display('home')

    def categories(self):
        inputParams = self.getInput()

        try:
            parent = inputParams['parent']
            order = int(inputParams['order']) if inputParams.has_key('order') else -1
            categoriesList = Categories.select().where(Categories.parent==parent)
            self.privData['CATEGORIES_LIST'] = categoriesList
            self.privData['ORDER'] = order
            return self.display('categories-list')
        except Exception, e:
            return self.error(msg='获取分类列表失败: %s' % e)


    def signin(self):
        from hashlib import md5
        inputs = self.getInput()

        try:
            username = inputs['username']
            password = md5(inputs['password']).hexdigest()
            user = Users.get(Users.name == username)
            if user.password != password:
                return self.error(msg='登录失败!')

            self.setLogin(username)
            user.last_login_time = datetime.now()
            user.save()
            self.notifications_list()
            return self.display('home')
        except Exception, e:
            print e
            return self.error(msg='登录失败!')
 
    def select_order(self):
        inputs = self.getInput()
        if inputs.has_key('query'):
            return self.orders_list()

        try:
            price, product_id = inputs['product'].split(' ')
            product = Products.get(Products.id == int(product_id))
            order = int(inputs['order'])

            if order > 0:
                details = OrderDetails.create(
                    name = product.category.name +"   "+product.diameter,
                    product = product,
                    count = 1,
                    price = price,
                    ratio = 0.0,
                    order = order,
                )
                return web.seeother(self.makeUrl('/wap/edit_price_sheet', {'id': order}))
            else:
                ordersList = Orders.select().order_by(Orders.id.desc())
                self.privData['ORDERS_LIST'] = ordersList
                self.privData['PRICE'] = price
                self.privData['PRODUCT'] = product
                return self.display('select-order')
        except Exception, e:
            print e
            return self.error(msg='加入订单失败!')

    def edit_my_information(self):
        inputs = self.getInput()
        try:
            user = Users.get(Users.id == inputs['id'])
            self.privData['USER'] = user
            return self.display('edit-my-information')
        except Exception,e:
            return self.error(msg='获取当前用户信息失败!')

    def edit_price_sheet(self):
        inputs = self.getInput()
        try:
            #import pdb; pdb.set_trace()
            order = Orders.get(Orders.id == int(inputs['id']))
            details = OrderDetails.select().where(OrderDetails.order == order).order_by(OrderDetails.id.desc())
            for each_d in details:
                print each_d.name
                print each_d.flag
            self.privData['ORDER'] = order
            self.privData['DETAILS'] = details
            return self.display('edit-price-sheet')
        except Exception,e:
            print e
            return self.error(msg='获取报价单详情信息失败!')
    
    def intro(self):
        return self.display('intro')
    
    def contacts_list(self):        
        try:
            contactsList = Contacts.select().order_by(Contacts.name)
            self.privData['CONTACTS_LIST'] = contactsList
            return self.display('contacts-list')
        except Exception, e:
            return self.error(msg='获取通讯录列表失败!')

    def contact_details(self):
        inputParams = self.getInput()

        try:
            contact = Contacts.get(Contacts.id == int(inputParams['id']))
            contact.description = self.htmlunescape(contact.description)
            self.privData['CONTACT_DETAILS'] = contact
            return self.display('contact-details')
        except Exception, e:
            print e
            return self.error(msg='获取联系人详情失败!')
 
    def news_list(self):
        try:
            newsList = News.select().order_by(News.id.desc())
            self.privData['NEWS_LIST'] = newsList
            return self.display('news-list')
        except Exception, e:
            return self.error(msg='获取行业动态列表失败!')

    def news_details(self):
        inputParams = self.getInput()
        try:
            newsDetails = News.get(News.id == int(inputParams['id']))
            newsDetails.content = self.htmlunescape(newsDetails.content)
            newsDetails.createTime = newsDetails.createTime.strftime('%Y-%m-%d')
            self.privData['NEWS_DETAILS'] = newsDetails
            return self.display('news-details')
        except Exception, e:
            return self.error(msg='获取行业动态详情失败!')
   
    def product_prices(self):
        inputParams = self.getInput()
        try:
            productsList = Products.select().where(Products.category==int(inputParams['category'])).order_by(Products.id.desc())
            self.privData['PRODUCTS_LIST'] = productsList
            self.privData['ORDER'] = int(inputParams['order']) if inputParams.has_key('order') else -1
            self.privData['CATEGORY'] = Categories.get(Categories.id==int(inputParams['category']))
            return self.display('product-prices')
        except Exception, e:
            print e
            return self.error(msg='获取产品价格列表失败!')

    def prices_list(self):
        return self.display('prices-list')

    def orders_list(self):
        try:
            #import pdb; pdb.set_trace()
            user = Users.get(Users.name == self.isLogin())
            ordersList = Orders.select().where(Orders.owner == user).order_by(Orders.id.desc())
            self.privData['ORDERS_LIST'] = ordersList
            return self.display('orders-list')
        except Exception, e:
            print e
            return self.error(msg='获取报价单列表失败!')

    def notifications_list(self):
        try:
            notificationsList = Notifications.select().order_by(Notifications.id.desc())
            self.privData['NOTIFICATIONS_LIST'] = notificationsList
            return self.display('notifications-list')
        except Exception, e:
            return self.error(msg='获取内部公告列表失败!')
    
    def notification_details(self):
        inputParams = self.getInput()
        try:
            notificationDetails = Notifications.get(Notifications.id == int(inputParams['id']))
            notificationDetails.content = self.htmlunescape(notificationDetails.content)
            notificationDetails.createTime =  notificationDetails.createTime.strftime('%Y-%m-%d')
            self.privData['NOTIFICATION'] = notificationDetails
            return self.display('notification-details')
        except Exception, e:
            return self.error(msg='获取内部公告详情失败!')

    def about_us(self):
        try:
            newsList = News.select().order_by(News.id.desc())
            self.privData['NEWS_LIST'] = newsList
            return self.display('about-us')
        except Exception, e:
            return self.error(msg='获取企业资质相关列表失败!')

    def honors(self):
        return self.display('honors')

    def contact_us(self):
        return self.display('contact-us')

    def my_information(self):
        try:
            user =Users.get(Users.name == self.isLogin())
            self.privData['USER'] = user
            return self.display('my-information')
        except Exception, e:
            print e
            return self.error(msg='获取用户信息失败!')

    def accountings_list(self):
        try:
            accountingsList = Accountings.select().order_by(Accountings.id.desc())
            self.privData['ACCOUNTINGS_LIST'] = accountingsList
            return self.display('accountings-list')
        except Exception, e:
            print e
            return self.error(msg='获取对帐单列表失败!')

    def accounting_details(self):
        inputParams = self.getInput()
        try:
            accounting = Accountings.get(Accountings.id == int(inputParams['id']))
            incommings = AccountIncommings.select().where(AccountIncommings.accounting==accounting).order_by(AccountIncommings.id.desc())
            outgoings = AccountOutgoings.select().where(AccountOutgoings.accounting==accounting).order_by(AccountOutgoings.id.desc())
            self.privData['ACCOUNTING'] = accounting
            self.privData['OUTGOINGS'] = outgoings
            self.privData['INCOMMINGS'] = incommings
            return self.display('accounting-details')
        except Exception, e:
            return self.error(msg='获取对帐单详情失败!')

    def confirm_accountings(self):
        inputs = self.getInput()
        status = 2 # disagree
        if inputs.has_key('agree'):
            status = 1

        try:
            accounting = Accountings.get(Accountings.id == int(inputs['id']))
            accounting.remark=inputs['remark']
            accounting.status=status
            accounting.save()
            return self.accountings_list()
        except Exception, e:
            print e
            return self.error(msg='确认对帐单失败!')

    def price_sheet_details(self):
        inputParams = self.getInput()
        try:
            #import pdb;pdb.set_trace();
            order = Orders.get(Orders.id == int(inputParams['id']))
            details = OrderDetails.select().where(OrderDetails.order == order).order_by(OrderDetails.id.desc())
            for od in details:
                print od.product.diameter
            self.privData['ORDER'] = order
            self.privData['DETAILS'] = details
            return self.display('price-sheet-details')
        except Exception, e:
            print e
            return self.error(msg='获取订单详情失败!')

    def export_price_sheet(self):
        inputParams = self.getInput()
        try:
            order = Orders.get(Orders.id == int(inputParams['id']))
            details = OrderDetails.select().where(OrderDetails.order == order).order_by(OrderDetails.id.desc())
            self.privData['ORDER'] = order
            self.privData['DETAILS'] = details
            import pdfcrowd
            # create an API client instance
            client = pdfcrowd.Client("luo_brian", "8fee9a05739553c92673004a3ec80201")

            # convert an HTML string and save the result to a file
            import os
            import config
            import utils
           
            tmpFile = os.path.join(config.UPLOAD_DIR, 'temp', '%s.pdf' % utils.uuidgen())
            ofile = open(tmpFile, 'wb')
            html = self.display('price-sheet-details-pdf')
            #html="<head></head><body>我的转换</body>"
            client.convertHtml(html, ofile)
            ofile.close()
            buf = open(tmpFile).read()
            os.unlink(tmpFile)
            web.header('Content-Type', 'application/pdf') 
            return buf
        except Exception, e:
            print e
            return self.error(msg='获取订单详情失败!')
