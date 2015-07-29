# -*- coding: utf-8 -*-
#coding=utf-8

from actions.base import jsonAction
from log import log
from config import COUNT_PER_PAGE
from models.albums import Albums
from models.images import Images
from models.categories import Categories
from models.groups import Groups
from models.products import Products
from models.articles import Articles
from models.chatrooms import Chatrooms
from models.users import Users
from models.product_favorites import ProductFavorites
from models.article_favorites import ArticleFavorites
from models.group_favorites import GroupFavorites
from models.group_comments import GroupComments
from models.product_comments import ProductComments
from models.questions import Questions
from models.answners import Answners
from models.group_rankings import GroupRankings
from models.product_rankings import ProductRankings
from models.transactions import Transactions
from models.group_payments import GroupPayments
from models.product_payments import ProductPayments

import utils
import web
import urllib2
import json
import urllib
import sys
import hashlib
import datetime
import time
import random as rand

def category_recursive_name(category):
    names = []
    while category and category.id != 1:   
        names.insert(0, category.name)
        category = category.parent

    return " : ".join(names)

def distance_to_str(distance):
    if not distance:
        return "未知距离"
    if int(distance/1000) > 0:
        return "%.2f 千米" % float(distance/1000.0)
    elif distance > .0:
        return "%d 米" % int(distance)

def gen_token():
    r = rand.random()
    return str(hashlib.sha1('%f%s'%(r, time.ctime())).hexdigest())

class jsonEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, datetime.date):
            return obj.strftime('%Y-%m-%d')
        elif isinstance(obj, decimal.Decimal):
            return float(obj)
        return json.JSONEncoder.default(self, obj)


'''
Ajax Actions
'''
class apiActions(jsonAction):
    def __init__(self):
        jsonAction.__init__(self)

    def GET(self, name):
        if name == 'albums':
            return self.albums()
        elif name == 'images':
            return self.images()
        elif name == 'categories':
            return self.categories()
        elif name == 'groups':
            return self.groups()
        elif name == 'groupinfo':
            return self.groupinfo()
        elif name == 'products':
            return self.products()
        elif name == 'productinfo':
            return self.productinfo()
        elif name == 'articleinfo':
            return self.articleinfo()
        elif name == 'userinfo':
            return self.userinfo()
        elif name == 'articles':
            return self.articles()
        elif name == 'chatroominfo':
            return self.chatroominfo()
        elif name == 'chatrooms':
            return self.chatrooms()
        elif name == 'users':
            return self.users()
        # 我收藏的公司
        elif name == 'favorite_groups':
            return self.favorite_groups()
        # 我收藏的产品
        elif name == 'favorite_products':
            return self.favorite_products()
        # 我收藏的文章
        elif name == 'favorite_articles':
            return self.favorite_articles()
        # 我的公司评论
        elif name == 'group_comments':
            return self.group_comments()
        # 我的产品评论
        elif name == 'product_comments':
            return self.product_comments()
        # 我的公司评论列表
        elif name == 'my_group_comments':
            return self.my_group_comments()
        # 我的产品评论列表
        elif name == 'my_product_comments':
            return self.my_product_comments()
        # 我的公司评分
        elif name == 'group_rankings':
            return self.group_rankings()
        # 我的产品评分 
        elif name == 'product_rankings':
            return self.product_rankings()   
        # 我的提问列表
        elif name == 'questions':
            return self.questions()
        # 问题详情
        elif name == 'questioninfo':
            return self.questioninfo()
        # 提问回答列表
        elif name == 'answners':
            return self.answners()
        # 我的订单列表
        elif name == 'transactions':
            return self.transactions()
        # 我的订单详情
        elif name == 'transaction_info':
            return self.transaction_info()

        return self.notFound()

    def POST(self, name):
        # 用户登录
        if name == 'signin':
            return self.signin()
        # 用户登出
        elif name == 'signout':
            return self.signout() 
        # 修改用户资料
        elif name == 'update_userinfo':
            return self.update_userinfo()
        # 用户注册
        elif name == 'signup':
            return self.signup()
        # 收藏公司
        elif name == 'like_group':
            return self.like_group()
        # 收藏产品 
        elif name == 'like_product':
            return self.like_product()
        # 评论公司
        elif name == 'comment_group':
            return self.comment_group()
        # 收藏文章 
        elif name == 'like_article':
            return self.like_article()
        # 评论产品
        elif name == 'comment_product':
            return self.comment_product()
        # 评价公司
        elif name == 'rank_group':
            return self.rank_group()
        # 评价产品
        elif name == 'rank_product':
            return self.rank_product()
        # 提问
        elif name == 'raise_question':
            return self.raise_question()
        # 修改密码
        elif name == 'update_userpw':
            return self.update_userpw()
        # 上传用户头像
        elif name == 'update_user_image':
            return self.update_user_image()
        # 上传问题图片
        elif name == 'upload_question_image':
            return self.upload_question_image()
        # 申请验证短信
        elif name == 'request_sms':
            return self.request_sms()
        # 取消收藏班级
        elif name == 'unlike_group':
            return self.unlike_group()
        # 取消收藏课程
        elif name == 'unlike_product':
            return self.unlike_product()
        # 取消收藏文章
        elif name == 'unlike_article':
            return self.unlike_article()

        return self.notFound()
        
    def albums(self):
        inputs = self.getInput()
        page = int(inputs['page']) if inputs.has_key('page') else 0
        offset = int(inputs['offset']) if inputs.has_key('offset') else 0
        limit = int(inputs['limit']) if inputs.has_key('limit') else COUNT_PER_PAGE

        albumsList = Albums.select(
                            Albums.id, 
                            Albums.thumbnail, 
                            Albums.name, 
                            Albums.description).where(Albums.id>1)

        if page:
            albumsList = albumsList \
                                .order_by(Albums.id.desc()) \
                                .paginate(page, limit)
        elif offset:
            albumsList  = albumsList.where(Albums.id>offset) \
                                .order_by(Albums.id.desc())

        return json.dumps([
                   {
                        'id': album.id,
                        'thumbnail': album.thumbnail,
                        'name': album.name,
                        'description': album.description
                    } for album in albumsList])

    def categories(self):
        inputs = self.getInput()
        parent = int(inputs['parent']) if inputs.has_key('parent') else 1
        page = int(inputs['page']) if inputs.has_key('page') else 0
        offset = int(inputs['offset']) if inputs.has_key('offset') else 0
        limit = int(inputs['limit']) if inputs.has_key('limit') else COUNT_PER_PAGE

        categoriesList = Categories.select()
        if page:
            categoriesList = categoriesList \
                                .where(Categories.parent == parent) \
                                .order_by(Categories.id.desc()) \
                                .paginate(page, limit)
        elif offset:
            categoriesList  = categoriesList \
                                .where(Categories.parent == parent, Categories.id > offset) \
                                .order_by(Categories.id.desc())

        return json.dumps([{
                    'id': category.id,
                    'name': category.name,
                    'thumbnail': category.thumbnail, 
                    'description': self.subText(self.htmlunquote(category.description), 0, 32),
                    'children': category.children.count(),
                } for category in categoriesList])

    def images(self):
        inputs = self.getInput()
        album = int(inputs['album']) if inputs.has_key('album') else 0
        offset = int(inputs['offset']) if inputs.has_key('offset') else 0
        page = int(inputs['page']) if inputs.has_key('page') else 0
        limit = int(inputs['limit']) if inputs.has_key('limit') else COUNT_PER_PAGE
        
        imagesList = Images.select(
)
        if album:
            imagesList = imagesList.where(Images.album == album) 

        if page:
            imagesList = imagesList.order_by(Images.id.desc()).paginate(page, limit)
        elif offset:
            imagesList  = imagesList.where(Images.id > offset).order_by(Images.id.desc())

        return json.dumps([
                {
                    'id': image.id,
                    'thumbnail': image.thumbnail,
                    'album': image.album.name,
                    'description': self.subText(self.htmlunquote(image.description), 0, 24),
                    'uuid': image.uuid,
                } for image in imagesList])


    def signin(self):
        from hashlib import md5
        inputs = self.getInput()

        try:
            cellphone = inputs['cellphone']
            password = md5(inputs['password']).hexdigest()
            user = Users.get(Users.cellphone == cellphone)

            if not user or user.role.type != 100 or user.password != password:
                return self.forbidden()

            t = int(time.time())
            if not user.token or t-time.mktime(user.token_created_time.timetuple()) > 144000:
                token = gen_token()
                user.token = token
                user.token_created_time = datetime.datetime.now()
            else:
                token = user.token
            
            user.last_login_time = datetime.datetime.now()
            user.save()
            return json.dumps({'token': token})
        except Exception, e:
            print e
            return self.error()

    def signup(self):        
        inputs = self.getInput()

        try:
            cellphone = inputs['cellphone']
            smscode = inputs['smscode']
            import leancloud
            if not leancloud.Apis().verify_sms_code(cellphone, smscode):
                return self.forbidden()
            
            from hashlib import md5
            password = md5(inputs['password']).hexdigest()

            token = gen_token()
            
            import base64
            from imaging import imaging

            Users.create(
                cellphone=cellphone, 
                name=cellphone,
                password=password,
                email = '%s@126.com' % cellphone,
                gender = 0,
                role = 3,
                description = '',
                avatur = base64.b64encode(buffer(imaging.default_thumbnail())),
                token = token,
            )

            return json.dumps({'token': token})
        except Exception, e:
            return self.error()


    def signout(self):
        inputs = self.getInput()

        try:
            token = inputs['token']
            user = Users.get(Users.token == token)
            user.token = None
            user.save()

            return self.success()
        except Exception, e:
            return self.error()

    def update_userinfo(self):
        inputs = self.getInput()

        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            if inputs.has_key('name'):
                user.name = inputs['name']

            if inputs.has_key('description'):
                user.description = inputs['description']

            if inputs.has_key('gender'):
                user.gender = int(inputs['gender'])

            if inputs.has_key('email'):
                user.email = inputs['email']

            user.save()
            return self.success()
        except Exception, e:
            return self.error()

    def groups(self):
        inputs = self.getInput()
        page = int(inputs['page']) if inputs.has_key('page') else 0
        category = int(inputs['category']) if inputs.has_key('category') else 0
        user = int(inputs['user']) if inputs.has_key('user') else 0
        latitude = float(inputs['latitude']) if inputs.has_key('latitude') else 0
        longitude = float(inputs['longitude']) if inputs.has_key('longitude') else 0
        offset = int(inputs['offset']) if inputs.has_key('offset') else 0
        limit = int(inputs['limit']) if inputs.has_key('limit') else COUNT_PER_PAGE
        distance = int(inputs['distance']) if inputs.has_key('distance') else 0
        keywords = inputs['keywords'] if inputs.has_key('keywords') else None
        
        groupsList = Groups.select() 

        if longitude and latitude:
            # 百度坐标转化成高德坐标
            latitude, longitude = utils.bd_decrypt(latitude, longitude)

        if category:
            groupsList = groupsList.where(Groups.category == category)
        elif user:
            groupsList = groupsList.where(Groups.owner == user)

        if keywords:
            groupsList = groupsList.where(Groups.name.contains(keywords))

        if page:
            groupsList = groupsList \
                                .order_by(Groups.id.desc()) \
                                .paginate(page, limit)
        elif offset:
            groupsList  = groupsList.where(Groups.id>offset) \
                                .order_by(Groups.id.desc())
        elif distance:
            groupsList = [group for group in groupsList 
                    if utils.distance(latitude, longitude, group.latitude, group.longitude) < distance]

        result = [{
            'id': group.id,
            'name': group.name,
            'description': self.subText(self.htmlunquote(group.description), 0, 32),
            'thumbnail': group.thumbnail.thumbnail,
            'image': group.thumbnail.uuid,
            'category': group.category.name,
            'specials': group.specials,
            'longitude': group.longitude,
            'latitude': group.latitude,
            'contact': group.contact,
            'phoneno': group.phoneno,
            'address': group.address,
            'distance': distance_to_str(utils.distance(latitude, longitude, group.latitude, group.longitude)),
            'price1': group.price1,
            'price2': group.price2,
            'favorites': GroupFavorites.select().where(GroupFavorites.group==group).count(),
            'comments': GroupComments.select().where(GroupComments.group==group).count(),
         } for group in groupsList]

        return json.dumps(result)

    def groupinfo(self):
        inputs = self.getInput()
        is_favorite = False

        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            pass

        try:
            favorite = GroupFavorites.get(
                GroupFavorites.owner == user,
                GroupFavorites.group == int(inputs['id'])
            )
            is_favorite = True            
        except Exception, e:
            pass

        try:
            group = Groups.get(Groups.id == (int(inputs['id'])))
            favorites = GroupFavorites.select().where(GroupFavorites.group == group).count()
            count = GroupComments.select().where(GroupComments.group == group.id).count()
            

            if  count == 0:
                avg = 4
            else:
                commentList = GroupComments.select().where(GroupComments.group==group.id)
                sum = 0
                for comment in commentList:
                    sum += comment.value

                avg = sum/count

            return json.dumps(
                       {
                           'id': group.id,
                           'image': group.thumbnail.uuid,
                           'name': group.name,
                           'owner': group.owner.name,
                           'description': self.htmlunescape(group.description),
                           'team_description': self.htmlunescape(group.team_description),
                           'thumbnail': group.thumbnail.thumbnail,
                           'category': group.category.name,
                           'specials': group.specials,
                           'service_modes': group.service_modes,
                           'regions': group.regions,
                           'price1': group.price1,
                           'price2': group.price1,
                           'faxno': group.faxno,
                           'postcode': group.postcode,
                           'longitude': group.longitude,
                           'latitude': group.latitude,
                           'contact': group.contact,
                           'phoneno': group.phoneno,
                           'cellphone': group.cellphone,
                           'address': group.address,
                           'is_favorite': is_favorite,
                           'count': count,
                           'favorites': favorites,
                           'swipeshow_album': group.swipeshow_album.id,
                           'groups_album': group.groups_album.id,
                           'avg': avg
                      })
        except Exception, e:
            print e
            return self.error()

    def products(self):
        inputs = self.getInput()
        group = int(inputs['group']) if inputs.has_key('group') else 0
        page = int(inputs['page']) if inputs.has_key('page') else 0
        offset = int(inputs['offset']) if inputs.has_key('offset') else 0
        limit = int(inputs['limit']) if inputs.has_key('limit') else COUNT_PER_PAGE
        latitude = float(inputs['latitude']) if inputs.has_key('latitude') else 0
        longitude = float(inputs['longitude']) if inputs.has_key('longitude') else 0
        distance = float(inputs['distance']) if inputs.has_key('distance') else 0
        keywords = inputs['keywords'] if inputs.has_key('keywords') else None   
        productsList = Products.select() 
       
        if longitude and latitude:
            # 百度坐标转化成高德坐标
            latitude, longitude = utils.bd_decrypt(latitude, longitude)        

        if group:
            productsList = productsList.where(Products.group == group)

        if keywords:
            productsList = productsList.where(Products.name.contains(keywords))

        if page:
            productsList = productsList.order_by(Products.id.desc()).paginate(page, limit)
        elif offset:
            productsList  = productsList.where(Products.id > offset).order_by(Products.id.desc())
        elif distance:
            productsList = [product for product in productsList
                    if utils.distance(latitude, longitude, product.latitude, product.longitude) < distance]

        return json.dumps([{
                        'name': product.name, 
                        'description': self.subText(self.htmlunquote(product.description), 0, 32), 
                        'thumbnail': product.thumbnail.thumbnail,
                        'id': product.id,
                        'price': product.price,
                        'discount': product.discount,
                        'category': product.category.name,
                        'group': product.group.name,
                        'longitude':product.longitude,
                        'latitude':product.latitude,
                        'distance': distance_to_str(utils.distance(latitude, longitude, product.latitude, product.longitude)),
                        'favorites': ProductFavorites.select().where(ProductFavorites.product==product).count(),
                        'comments': ProductComments.select().where(ProductComments.product==product).count(),
                    } for product in productsList], cls = jsonEncoder)

    def productinfo(self):
        inputs = self.getInput()
        is_favorite = False

        try:
            user = Users.get(Users.token == inputs['token'])
            favorite = ProductFavorites.get(
                ProductFavorites.owner == user,
                ProductFavorites.product == int(inputs['id'])
            )
            is_favorite = True            
        except Exception, e:
            pass

 
        try:
            product = Products.get(Products.id == int(inputs['id']))
            favorites = ProductFavorites.select().where(ProductFavorites.product == product).count()
            count = ProductComments.select().where(ProductComments.product == product.id).count()


            if  count == 0:
                avg = 4
            else:
                commentList = ProductComments.select().where(ProductComments.product==product.id)
                sum = 0
                for comment in commentList:
                    sum += comment.value

                avg = sum/count

            return json.dumps(
                     {
                        'name': product.name,
                        'image': product.thumbnail.uuid, 
                        'description': self.htmlunescape(product.description),
                        'team_description':product.team_description, 
                        'thumbnail': product.thumbnail.thumbnail,
                        'id': product.id,
                        'is_favorite': is_favorite,
                        'price': product.price,
                        'discount': product.discount,
                        'category': product.category.name,
                        'group': product.group.name,
                        'created_time': product.created_time,
                        'owner': product.owner.name,
                        'longitude': product.longitude,
                        'latitude': product.latitude,
                        'address': product.address,
                        'contact': product.contact,
                        'phoneno': product.phoneno,
                        'cellphone': product.cellphone,
                        'faxno': product.faxno,
                        'postcode': product.postcode,
                        'products_album': product.products_album.id,
                        'swipeshow_album': product.swipeshow_album.id,
                        'regions': product.regions,
                        'service_modes': product.service_modes,
                        'specials': product.specials,     
                        'video_name': product.video_name,
                        'video_desc': product.video_desc,
                        'video_url': product.video_url,
                        'video_mobile_url': product.video_mobile_url,
                        'video_adaptive_url': product.video_mobile_url,
                        'video_rate': product.video_rate,
                        'video_width': product.video_width,
                        'video_height': product.video_height,
                        'video_thumbnail': product.video_thumbnail,
                        'video_uptime': product.video_uptime,
                        'video_duration': product.video_duration,
                        'favorites': favorites,
                        'avg': avg
                     },cls = jsonEncoder)
        except Exception, e:
            print e
            return self.error()

    def articles(self):
        inputs = self.getInput()
        category = int(inputs['category']) if inputs.has_key('category') else 0
        page = int(inputs['page']) if inputs.has_key('page') else 0
        offset = int(inputs['offset']) if inputs.has_key('offset') else 0
        limit = int(inputs['limit']) if inputs.has_key('limit') else COUNT_PER_PAGE

        articlesList = Articles.select()
        if category:
            articlesList = articlesList.where(Articles.category == category)

        if page:
            articlesList = articlesList \
                                .order_by(Articles.id.desc()) \
                                .paginate(page, limit)
        elif offset:
            articlesList  = articlesList.where(Articles.id > offset) \
                                .order_by(Articles.id.desc())

        return json.dumps([
                    {
                        'id': article.id,
                        'name': article.name,
                        'thumbnail': article.thumbnail.thumbnail,
                        'content': self.subText(self.htmlunquote(article.content), 0, 32),
                    } for article in articlesList])


    def articleinfo(self):
        inputs = self.getInput()
        is_favorite = False
        try:
            user = Users.get(Users.token == inputs['token'])
            article = Articles.get(Articles.id == (int(inputs['id'])))
            favorite = ArticleFavorites.get(
                ArticleFavorites.owner == user,
                ArticleFavorites.article == int(inputs['id'])
            )
            is_favorite = True         
  
        except Exception, e:
            pass


        try:
            article = Articles.get(Articles.id == (int(inputs['id'])))
            return json.dumps(
                    {
                        'is_favorite': is_favorite,
                        'id': article.id,
                        'category': article.category.name,
                        'name': article.name,
                        'content': self.htmlunescape(article.content)
                    })
        except Exception, e:
            return self.error()

    def userinfo(self):
        inputs = self.getInput()
        # 检查用户是否登录，否则返回403错误，前台需要切换到
        # login界面
        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        return json.dumps({
                   'id': user.id,
                   'cellphone': user.cellphone,
                   'name': user.name,
                   'avatur': user.avatur, 
                   'email': user.email,
                   'description': self.htmlunquote(self.htmlunescape(user.description)),
                   'gender': user.gender
               })

    def favorite_products(self):
        inputs = self.getInput()
        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            page = int(inputs['page']) if inputs.has_key('page') else 0
            offset = int(inputs['offset']) if inputs.has_key('offset') else 0
            limit = int(inputs['limit']) if inputs.has_key('limit') else COUNT_PER_PAGE

            favsList = ProductFavorites.select().where(ProductFavorites.owner==user)
            if page:
                favsList = favsList \
                                .order_by(ProductFavorites.id.desc()) \
                                .paginate(page, limit)
            elif offset:
                favsList  = favsList.where(ProductFavorites.id > offset) \
                                .order_by(ProductFavorites.id.desc())

            return json.dumps([
                    {
                        'id': fav.id,
                        'user': user.id,
                        'product': fav.product.id,
                        'price': fav.product.price,
                        'name': fav.product.name,
                        'group_name': fav.product.group.name,
                        'created_time': fav.created_time,
                        'thumbnail': fav.product.thumbnail.thumbnail,
                        'category': fav.product.category.name,
                        'description': self.subText(self.htmlunquote(fav.product.description), 0, 32),
                    } for fav in favsList], cls=jsonEncoder)
        except Exception, e:
            return self.error()

    def favorite_groups(self):
        inputs = self.getInput()
        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            page = int(inputs['page']) if inputs.has_key('page') else 0
            offset = int(inputs['offset']) if inputs.has_key('offset') else 0
            limit = int(inputs['limit']) if inputs.has_key('limit') else COUNT_PER_PAGE
            latitude = float(inputs['latitude']) if inputs.has_key('latitude') else 0
            longitude = float(inputs['longitude']) if inputs.has_key('longitude') else 0

            if longitude and latitude:
                # 百度坐标转化成高德坐标
                latitude, longitude = utils.bd_decrypt(latitude, longitude)

            favsList = GroupFavorites.select().where(GroupFavorites.owner==user)
            if page:
                favsList = favsList \
                                .order_by(GroupFavorites.id.desc()) \
                                .paginate(page, limit)
            elif offset:
                  favsList  = favsList.where(GroupFavorites.id > offset) \
                                .order_by(GroupFavorites.id.desc())

            return json.dumps([
                    {
                        'id': fav.id,
                        'group': fav.group.id,
                        'name': fav.group.name,
                        'created_time': fav.created_time,
                        'thumbnail': fav.group.thumbnail.thumbnail,
                        'category': fav.group.category.name,
                        'specials': fav.group.specials,
                        'longitude': fav.group.longitude,
                        'latitude': fav.group.latitude,
                        'contact': fav.group.contact,
                        'phoneno': fav.group.phoneno,
                        'address': fav.group.address,
                        'distance': distance_to_str(utils.distance(latitude, longitude, fav.group.latitude, fav.group.longitude)),
                     #  'price_home_service': fav.group.price_home_service,
                     #  'price_remote_service': fav.group.price_remote_service,
                        'description': self.subText(self.htmlunquote(fav.group.description), 0, 32),
                        'favorites': GroupFavorites.select().where(GroupFavorites.group==fav.group).count(),
                        'comments': GroupComments.select().where(GroupComments.group==fav.group).count(),
                    } for fav in favsList], cls=jsonEncoder)
        except Exception,e:
             return self.error()

    def like_group(self):
        inputs = self.getInput()

        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            group = inputs['group']            
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            fav = GroupFavorites.get_or_create(
                    owner=user, 
                    group=group,
                  )
            return self.success()
        except Exception, e:
            return self.error()

    def like_product(self):
        inputs = self.getInput()

        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            product = inputs['product']
            fav = ProductFavorites.get_or_create(
                    owner=user, 
                    product=product,
                  )
            return self.success()
        except Exception, e:
            return self.error()

    def like_article(self):
        inputs = self.getInput()

        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            article = inputs['article']
            fav = ArticleFavorites.get_or_create(
                    owner=user,
                    article=article,
                  )
            return self.success()
        except Exception, e:
            return self.error()


    def unlike_article(self):
        inputs = self.getInput()

        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            fav = ArticleFavorites.get(
                    owner=user,
                    article=int(inputs['article']),
                  )
            fav.delete_instance()
            return self.success()
        except Exception, e:
            return self.error()

    def group_comments(self):
        inputs = self.getInput()
        try:
            group = int(inputs['group'])
            page = int(inputs['page']) if inputs.has_key('page') else 0
            offset = int(inputs['offset']) if inputs.has_key('offset') else 0
            limit = int(inputs['limit']) if inputs.has_key('limit') else COUNT_PER_PAGE

            commentList = GroupComments.select().where(GroupComments.group==group)

            if page:
                commentList = commentList \
                                .order_by(GroupComments.id.desc()) \
                                .paginate(page, limit)
            elif offset:
                commentList  = commentList.where(GroupComments.id>offset) \
                                .order_by(GroupComments.id.desc())

            return json.dumps([
                    {
                        'id': comment.id,
                        'group': comment.group.id,
                        'user': comment.owner.name,
                        'created_time': str(comment.created_time)[:16],
                        'thumbnail': comment.owner.avatur,
                        'gender': comment.owner.gender,
                        'value':comment.value,
                        'content': self.subText(self.htmlunquote(comment.content), 0, 64),
                    } for comment in commentList], cls=jsonEncoder)
        except Exception, e:
            return self.error()

    def product_comments(self):
        inputs = self.getInput()
        try:
            product = int(inputs['product'])
            page = int(inputs['page']) if inputs.has_key('page') else 0
            offset = int(inputs['offset']) if inputs.has_key('offset') else 0
            limit = int(inputs['limit']) if inputs.has_key('limit') else COUNT_PER_PAGE

            commentList = ProductComments.select().where(ProductComments.product==product)
          
            if page:
                commentList = commentList \
                                .order_by(ProductComments.id.desc()) \
                                .paginate(page, limit)
            elif offset:
                commentList  = commentList.where(ProductComments.id>offset) \
                                .order_by(ProductComments.id.desc())
            for comment in commentList:
                print comment.id
                print comment.product.id
            return json.dumps([
                    {
                        'id': comment.id,
                        'product': comment.product.id,
                        'user': comment.owner.name,
                        'created_time': str(comment.created_time)[:16],
                        'thumbnail': comment.owner.avatur,
                        'gender': comment.owner.gender,
                        'starValue': comment.value,
                        'content': self.subText(self.htmlunquote(comment.content), 0, 64),
                    } for comment in commentList], cls=jsonEncoder)
        except Exception, e:
            return self.error()

    def comment_group(self):
        inputs = self.getInput()

        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            group = inputs['group']
            content = inputs['content']
            value = inputs['value']
            comment = GroupComments.get_or_create(
                    owner=user, 
                    group=group,
                    content=content,
                    value=value,
                  )
            return self.success()
        except Exception, e:
            return self.error()

    def comment_product(self):
        inputs = self.getInput()

        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            product = inputs['product']
            content = inputs['content']
            value = inputs['value']
            comment = ProductComments.get_or_create(
                    owner=user, 
                    product=product,
                    content=content,
                    value=value,
                  )
            return self.success()
        except Exception, e:
            return self.error()

    def questions(self):
        inputs = self.getInput()
        # 检查用户是否登录，否则返回403错误，前台需要切换到

        try:
            user = Users.get(Users.token == inputs['token']) if inputs.has_key('token') else None
            page = int(inputs['page']) if inputs.has_key('page') else 0
            offset = int(inputs['offset']) if inputs.has_key('offset') else 0
            limit = int(inputs['limit']) if inputs.has_key('limit') else COUNT_PER_PAGE

            questionsList = Questions.select()
            if user:
                questionsList = questionsList.where(Questions.owner==user)
                #questionsList = user.questions_owner
            if page:
                questionsList = questionsList \
                                .order_by(Questions.id.desc()) \
                                .paginate(page, limit)
            elif offset:
                questionsList  = questionsList.where(Questions.id>offset) \
                                .order_by(Questions.id.desc())

            return json.dumps([
                    {
                        'id': question.id,
                        'title': question.title,
                        'user': question.owner.name,
                        'thumbnail': question.owner.avatur,
                        'created_time': question.created_time,
                        'content': self.subText(self.htmlunquote(question.content), 0, 48),
                        'answners': Answners.select().where(Answners.question==question).count()
                    } for question in questionsList], cls=jsonEncoder)
        except Exception, e:
            return self.error()

    def questioninfo(self):
        inputs = self.getInput()

        try:
            question = Questions.get(
                    Questions.id == int(inputs['id'])
                  )
            album = question.album.id if question.album else 0

            return json.dumps({
                        'id': question.id,
                        'title': question.title,
                        'user': question.owner.name,
                        'thumbnail': question.owner.avatur,
                        'created_time': question.created_time,
                        'content': self.htmlunescape(question.content),
                        'album': album,
                }, cls=jsonEncoder)
        except Exception, e:
            return self.error()

    def answners(self):
        inputs = self.getInput()

        try:
            question = int(inputs['question']) if inputs.has_key('question') else 0
            page = int(inputs['page']) if inputs.has_key('page') else 0
            offset = int(inputs['offset']) if inputs.has_key('offset') else 0
            limit = int(inputs['limit']) if inputs.has_key('limit') else COUNT_PER_PAGE

            answnersList = Answners.select()
            if question:
                answnersList = answnersList.where(Answners.question == question)

            if page:
                answnersList = answnersList \
                                .order_by(Answners.id.desc()) \
                                .paginate(page, limit)
            elif offset:
                answnersList  = answnersList.where(Answners.id>offset) \
                                .order_by(Answners.id.desc())

            return json.dumps([
                    {
                        'id': answner.id,
                        'type': answner.type,
                        'user': answner.owner.name,
                        'thumbnail': answner.owner.avatur,
                        'created_time': answner.created_time,
                        'content': self.htmlunescape(answner.content),
                    } for answner in answnersList], cls=jsonEncoder)
        except Exception, e:
            return self.error()

    def raise_question(self):
        inputs = self.getInput()

        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            group = int(inputs['group'])
            title = inputs['title']
            content = inputs['content']
            album = int(inputs['album'])
            if album:
                question = Questions.get_or_create(
                        group=group,
                        owner=user, 
                        content=content,
                        title=title,
                        album=album,
                    )
            else:
                question = Questions.get_or_create(
                        group=group,
                        owner=user, 
                        content=content,
                        title=title,  
                    )
            return self.success()
        except Exception, e:
            print e
            return self.error()

    def group_rankings(self):
        inputs = self.getInput()
        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            page = int(inputs['page']) if inputs.has_key('page') else 0
            offset = int(inputs['offset']) if inputs.has_key('offset') else 0
            limit = int(inputs['limit']) if inputs.has_key('limit') else COUNT_PER_PAGE

            rankingList = GroupRankings.select().where(GroupRankings.owner==user)
            if page:
                rankingList = rankingList \
                                .order_by(GroupRankings.id.desc()) \
                                .paginate(page, limit)
            elif offset:
                rankingList  = rankingList.where(GroupRankings.id>offset) \
                                .order_by(GroupRankings.id.desc())

            return json.dumps([
                    {
                        'id': groupranking.id,
                        'user': user.id,
                        'created_time': groupranking.created_time,
                        'value': groupranking.value,
                        'group': groupranking.group.id,
                    } for groupranking in rankingList], cls=jsonEncoder)
        except Exception, e:
            return self.error()

    def product_rankings(self):
        inputs = self.getInput()
        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            page = int(inputs['page']) if inputs.has_key('page') else 0
            offset = int(inputs['offset']) if inputs.has_key('offset') else 0
            limit = int(inputs['limit']) if inputs.has_key('limit') else COUNT_PER_PAGE

            rankingList = ProductRankings.select().where(ProductRankings.owner==user)
            if page:
                rankingList = rankingList \
                                .order_by(ProductRankings.id.desc()) \
                                .paginate(page, limit)
            elif offset:
                rankingList  = rankingList.where(ProductRankings.id>offset) \
                                .order_by(ProductRankings.id.desc())

            return json.dumps([
                    {
                        'id': productranking.id,
                        'user': user.id,
                        'created_time': productranking.created_time,
                        'value': productranking.value,
                        'product': productranking.product.id,
                    } for productranking in rankingList], cls=jsonEncoder)
        except Exception, e:
            return self.error()  

    def rank_group(self):
        inputs = self.getInput()

        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            value = inputs['value']
            group = inputs['group']
            type = inputs['type']
            ranking = GroupRankings.get_or_create(
                    owner=user, 
                    value=value,
                    group=group,
                    type=type,
                  )
            return self.success()
        except Exception, e:
            return self.error() 

    def rank_product(self):
        inputs = self.getInput()

        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            product = inputs['product']
            value = inputs['value']
            type = inputs['type']
            rankings = ProductRankings.get_or_create(
                    owner=user, 
                    value=value,
                    product=product,
                    type=type,
                  )
            return self.success()
        except Exception, e:
            return self.error()  

    def update_userpw(self):
        from hashlib import md5
        inputs = self.getInput()

        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            user.password = md5(inputs['password']).hexdigest()
            user.save()

            return self.success()
        except Exception, e:
            return self.error()  

    def transactions(self):
        inputs = self.getInput()
        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            status =  int(inputs['status']) if inputs.has_key('status') else -1
            page = int(inputs['page']) if inputs.has_key('page') else 0
            offset = int(inputs['offset']) if inputs.has_key('offset') else 0
            limit = int(inputs['limit']) if inputs.has_key('limit') else COUNT_PER_PAGE

            transactionsList = Transactions.select().where(Transactions.owner==user)
            if status >=0:
                transactionsList = transactionsList.where(Transactions.trade_status == status)

            if page:
                transactionsList = transactionsList \
                                .order_by(Transactions.id.desc()) \
                                .paginate(page, limit)
            elif offset:
                transactionsList  = transactionsList.where(Transactions.id>offset) \
                                .order_by(Transactions.id.desc())

            ret = list()
            for t in transactionsList:
                try:
                    group = GroupPayments.get(GroupPayments.transaction==t).group
                    name = group.name
                    thumbnail = group.thumbnail.thumbnail
                    description = self.subText(self.htmlunquote(group.description), 0, 32),
                except Exception, e:
                    product = ProductPayments.get(ProductPayments.transaction==t).product
                    name = product.name
                    thumbnail = product.thumbnail.thumbnail
                    description = self.subText(self.htmlunquote(product.description), 0, 32),

                ret.append({
                        'id': t.id,
                        'name': name,
                        'created_time': t.created_time,
                        'trade_status' : t.trade_status,
                        'owner': t.owner.name,
                        'total_price': t.total_price, 
                        'thumbnail': thumbnail,
                        'description': description,
                    })

            return json.dumps(ret, cls=jsonEncoder)
        except Exception, e:
            return self.error()

    def transaction_info(self):
        inputs = self.getInput()
        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            t = Transactions.get(
                    Transactions.owner == user,
                    Transactions.id == int(inputs['id'])
                )
            return json.dumps({
                        'id': t.id,
                        'created_time': t.created_time,
                        'trade_status' : t.trade_status,
                        'ali_pay_trade_id': t.alipay_trade_id,
                        'last_modified_time': t.last_modified_time,
                        'owner': t.owner.name,
                        'cellphone': t.owner.cellphone,
                        'total_price': t.total_price, 
                        'groups': 
                            [{
                                'name': p.group.name,
                                'description':  self.subText(self.htmlunquote(p.group.description), 0, 32),
                                'thumbnail': p.group.thumbnail.thumbnail,
                                'type': p.type, 
                            } for p in t.group_payments_transaction],
                        'products': 
                            [{
                                'name': p.product.name,
                                'description': self.subText(self.htmlunquote(p.product.description), 0, 32),
                                'thumbnail': p.product.thumbnail.thumbnail,
                            } for p in t.product_payments_transaction],
                  }, cls=jsonEncoder)
        except Exception, e:
            return self.error()

    def update_user_image(self):
        inputParams = web.input()
        uploaded_file = None

        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputParams['token'])
        except Exception, e:
            return self.forbidden()

        import os, base64
        from imaging import imaging
        from uploadmgr import httpUploadedFile
        from config import IMAGE_XRES, IMAGE_YRES, THUMBNAIL_XRES, THUMBNAIL_YRES

        try:
            uploaded_file = httpUploadedFile(inputParams.file)
            if uploaded_file.mimetype() != 'image/jpeg':
                os.unlink(uploaded_file.target())
                return self.error()

            im = imaging(uploaded_file.target())
            tmpfile = uploaded_file.target() + ".tmp"
            data = im.resize(IMAGE_XRES, IMAGE_YRES)
            file(tmpfile, 'w').write(data)
            os.unlink(uploaded_file.target())
            os.rename(tmpfile, uploaded_file.target())

            thumbnail_blob = im.resize(THUMBNAIL_XRES, THUMBNAIL_YRES)
            thumbnail_data = base64.b64encode(buffer(thumbnail_blob))
            Images.get_or_create(
                uuid =  uploaded_file.uuid(),
                description = '%s上传的图片!' % user.name,
                album = 1,
                owner = user,
                thumbnail = thumbnail_data
            )

            user.avatur = thumbnail_data
            user.save()
        except Exception, e:
            if uploaded_file and os.path.exists(uploaded_file.target()):
                os.unlink(uploaded_file.target())
            return self.error()

    def upload_question_image(self):
        inputParams = web.input()
        uploaded_file = None
        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputParams['token'])
        except Exception, e:
            return self.forbidden()

        import os, base64
        from imaging import imaging

        try:
            album = Albums.get(Albums.id == int(inputParams['album']))
        except Exception, e:
            album = Albums.get_or_create(
                        name = '用户%s专辑@%s' % (user.name, str(datetime.datetime.now())),
                        description = '用户%s上传的专辑!' % user.name,
                        owner = user,
                        thumbnail = base64.b64encode(buffer(imaging.default_thumbnail()))
                    )
            pass

        from uploadmgr import httpUploadedFile
        from config import IMAGE_XRES, IMAGE_YRES, THUMBNAIL_XRES, THUMBNAIL_YRES

        try:
            uploaded_file = httpUploadedFile(inputParams.file)
            if uploaded_file.mimetype() != 'image/jpeg':
                os.unlink(uploaded_file.target())
                return self.error()

            im = imaging(uploaded_file.target())
            tmpfile = uploaded_file.target() + ".tmp"
            data = im.resize(IMAGE_XRES, IMAGE_YRES)
            file(tmpfile, 'w').write(data)
            os.unlink(uploaded_file.target())
            os.rename(tmpfile, uploaded_file.target())

            thumbnail_blob = im.resize(THUMBNAIL_XRES, THUMBNAIL_YRES)
            thumbnail_data = base64.b64encode(buffer(thumbnail_blob))
            image = Images.get_or_create(
                uuid =  uploaded_file.uuid(),
                description = '%s上传的图片!' % user.name,
                album = album,
                owner = user,
                thumbnail = thumbnail_data
            )
            return json.dumps({
                        'id': image.id,
                        'album': album.id,
                        'uuid': image.uuid,
                    })
        except Exception, e:
            if uploaded_file and os.path.exists(uploaded_file.target()):
                os.unlink(uploaded_file.target())
            return self.error()

    def request_sms(self):
        inputs = self.getInput()
        cellphone = inputs['cellphone']

        try:
            user = Users.get(Users.cellphone == cellphone)
            return self.forbidden()
        except Exception, e:
            try:
                import leancloud
                leancloud.Apis().request_sms_code(cellphone)
                return self.success()
            except Exception, e:
                return self.error()

    def unlike_group(self):
        inputs = self.getInput()

        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            fav = GroupFavorites.get(
                    owner=user, 
                    group=int(inputs['group']),
                  )
            fav.delete_instance()
            return self.success()
        except Exception, e:
            return self.error()


    def unlike_product(self):
        inputs = self.getInput()

        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            fav = ProductFavorites.get(
                    owner=user, 
                    product=int(inputs['product']),
                  )
            fav.delete_instance()
            return self.success()
        except Exception, e:
            return self.error()

    def my_group_comments(self):
        inputs = self.getInput()

        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            page = int(inputs['page']) if inputs.has_key('page') else 0
            offset = int(inputs['offset']) if inputs.has_key('offset') else 0
            limit = int(inputs['limit']) if inputs.has_key('limit') else COUNT_PER_PAGE
            commentList = GroupComments.select().where(GroupComments.owner==user)

            if page:
                commentList = commentList \
                                .order_by(GroupComments.id.desc()) \
                                .paginate(page, limit)
            elif offset:
                commentList  = commentList.where(GroupComments.id>offset) \
                                .order_by(GroupComments.id.desc())
             
            return json.dumps([
                    {
                        'id': comment.id,
                        'group': comment.group.id,
                        'group_name': comment.group.name,
                        'user': comment.owner.name,
                        'created_time': str(comment.created_time)[:16],
                        'thumbnail': comment.group.thumbnail.thumbnail,
                        'gender': comment.owner.gender,
                        'starValue': comment.value,
                        'content': self.subText(self.htmlunquote(comment.content), 0, 64),
                    } for comment in commentList], cls=jsonEncoder)
        except Exception, e:
            return self.error()
     
    def my_product_comments(self):
        inputs = self.getInput()

        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            page = int(inputs['page']) if inputs.has_key('page') else 0
            offset = int(inputs['offset']) if inputs.has_key('offset') else 0
            limit = int(inputs['limit']) if inputs.has_key('limit') else COUNT_PER_PAGE

            commentList = ProductComments.select().where(ProductComments.owner==user)

            if page:
                commentList = commentList \
                                .order_by(ProductComments.id.desc()) \
                                .paginate(page, limit)
            elif offset:
                commentList  = commentList.where(ProductComments.id>offset) \
                                .order_by(ProductComments.id.desc())

            return json.dumps([
                    {
                        'id': comment.id,
                        'product': comment.product.id,
                        'starValue': comment.value,
                        'product_name': comment.product.name,
                        'user': comment.owner.name,
                        'created_time': str(comment.created_time)[:16],
                        'thumbnail': comment.product.thumbnail.thumbnail,
                        'gender': comment.owner.gender,
                        'content': self.subText(self.htmlunquote(comment.content), 0, 64),
                    } for comment in commentList], cls=jsonEncoder)
        except Exception, e:
            return self.error()

    def chatrooms(self):
        inputs = self.getInput()
        page = int(inputs['page']) if inputs.has_key('page') else 0
        offset = int(inputs['offset']) if inputs.has_key('offset') else 0
        limit = int(inputs['limit']) if inputs.has_key('limit') else COUNT_PER_PAGE
        chatroomsList = Chatrooms.select()
        if page:
            chatroomsList = chatroomsList \
                                .order_by(Chatrooms.id.desc()) \
                                .paginate(page, limit)
        elif offset:
            chatroomsList  = chatroomsList.where(Chatrooms.id > offset) \
                                .order_by(Chatrooms.id.desc())

        return json.dumps([
                    {
                        'id': chatroom.id,
                        'name': chatroom.name,
                        'thumbnail': chatroom.thumbnail.thumbnail,
                        'uuid': chatroom.uuid,
                        'description': self.subText(self.htmlunquote(chatroom.description), 0, 32),
                    } for chatroom in chatroomsList])

    def chatroominfo (self):
        inputs = self.getInput()

        try:
            chatroom = Chatrooms.get(Chatrooms.id == (int(inputs['id'])))

            return json.dumps(
                    {
                        'id': chatroom.id,
                        'name': chatroom.name,
                        'thumbnail': chatroom.thumbnail.thumbnail,
                        'uuid': chatroom.uuid,
                        'description': self.subText(self.htmlunquote(chatroom.description), 0, 32),
                    })
        except Exception, e:
            return self.error()
    
    def favorite_articles(self):
        inputs = self.getInput()
        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
          # import pdb;pdb.set_trace()
            page = int(inputs['page']) if inputs.has_key('page') else 0
            offset = int(inputs['offset']) if inputs.has_key('offset') else 0
            limit = int(inputs['limit']) if inputs.has_key('limit') else COUNT_PER_PAGE

            favsList = ArticleFavorites.select().where(ArticleFavorites.owner==user)
            if page:
                favsList = favsList \
                                .order_by(ArticleFavorites.id.desc()) \
                                .paginate(page, limit)
            elif offset:
                favsList  = favsList.where(ArticleFavorites.id > offset) \
                                .order_by(ArticleFavorites.id.desc())

            return json.dumps([
                   { 
                        'id': fav.id,
                        'user': user.id,
                        'article': fav.article.id,
                        'name': fav.article.name,
                        'created_time': str(fav.created_time)[:16],
                        'thumbnail': fav.article.thumbnail.thumbnail,
                        'category': fav.article.category.name,
                        'content': self.subText(self.htmlunquote(fav.article.content), 0, 32),   
                    } for fav in favsList], cls=jsonEncoder)
        except Exception, e:
              print e
              return self.error()         
