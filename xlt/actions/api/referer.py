# -*- coding: utf-8 -*-
#coding=utf-8

from actions.base import jsonAction
from log import log
from config import COUNT_PER_PAGE
from models.albums import Albums
from models.images import Images
from models.categories import Categories
from models.groups import Groups
from models.courses import Courses
from models.agents import Agents
from models.users import Users
from models.course_favorites import CourseFavorites
from models.group_favorites import GroupFavorites
from models.group_comments import GroupComments
from models.course_comments import CourseComments
from models.questions import Questions
from models.answners import Answners
from models.group_rankings import GroupRankings
from models.course_rankings import CourseRankings
from models.group_enrollments import GroupEnrollments
from models.transactions import Transactions
from models.group_payments import GroupPayments
from models.course_payments import CoursePayments

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
        elif name == 'courses':
            return self.courses()
        elif name == 'courseinfo':
            return self.courseinfo()
        elif name == 'agentinfo':
            return self.agentinfo()
        elif name == 'userinfo':
            return self.userinfo()
        elif name == 'agents':
            return self.agents()
        elif name == 'users':
            return self.users()
        # 我收藏的班级
        elif name == 'favorite_groups':
            return self.favorite_groups()
        # 我收藏的课程
        elif name == 'favorite_courses':
            return self.favorite_courses()
        # 我的班级评论
        elif name == 'group_comments':
            return self.group_comments()
        # 我的课程评论
        elif name == 'course_comments':
            return self.course_comments()
        # 我的评论列表
        elif name == 'comments':
            return self.comments()
        # 我的班级评价
        elif name == 'group_rankings':
            return self.group_rankings()
        # 我的课程评价 
        elif name == 'course_rankings':
            return self.course_rankings()   
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
        # 我加入班级的列表
        elif name == 'enrollments':
            return self.enrollments()
        return self.notFound()

    def POST(self, name):
        if name == 'signin':
            return self.signin()
        elif name == 'signout':
            return self.signout() 
        elif name == 'update_userinfo':
            return self.update_userinfo()
        elif name == 'signup':
            return self.signup()
        # 收藏班级
        elif name == 'like_group':
            return self.like_group()
        # 收藏课程
        elif name == 'like_course':
            return self.like_course()
        # 评论班级
        elif name == 'comment_group':
            return self.comment_group()
        # 评论课程
        elif name == 'comment_course':
            return self.comment_course()
        # 评价班级
        elif name == 'rank_group':
            return self.rank_group()
        # 评价课程
        elif name == 'rank_course':
            return self.rank_course()
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
        # 加入班级
        elif name == 'enroll_group':
            return self.enroll_group()
        # 退出班级
        elif name == 'quit_group':
            return self.quit_group()
        # 取消收藏班级
        elif name == 'unlike_group':
            return self.unlike_group()
        # 取消收藏课程
        elif name == 'unlike_course':
            return self.unlike_course()

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
            'price_home_service': group.price_home_service,
            'price_remote_service': group.price_remote_service,
            'enrolls': GroupEnrollments.select().where(GroupEnrollments.group==group).count(),
            'favorites': GroupFavorites.select().where(GroupFavorites.group==group).count(),
            'comments': GroupComments.select().where(GroupComments.group==group).count(),
         } for group in groupsList]

        return json.dumps(result)

    def groupinfo(self):
        inputs = self.getInput()
        is_favorite = False
        is_enrolled = False

        try:
            user = Users.get(Users.token == inputs['token'])
            enrollment = GroupEnrollments.get(
                GroupEnrollments.owner == user, 
                GroupEnrollments.group == int(inputs['id'])
            )
            is_enrolled = True
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
            enrolls = GroupEnrollments.select().where(GroupEnrollments.group == group).count()
            favorites = GroupFavorites.select().where(GroupFavorites.group == group).count()
            count = GroupComments.select().where(GroupComments.group==group.id).count()

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
                           'name': group.name,
                           'description': self.htmlunescape(group.description),
                           'thumbnail': group.thumbnail.thumbnail,
                           'category': group.category.name,
                           'specials': group.specials,
                           'teaching_modes': group.teaching_modes,
                           'regions': group.regions,
                           'teaching_team': self.htmlunescape(group.teaching_team),
                           'chatroom': group.chatroom,
                           'chatroom_name': group.chatroom_name,
                           'price_home_service': group.price_home_service,
                           'price_remote_service': group.price_remote_service,
                           'longitude': group.longitude,
                           'latitude': group.latitude,
                           'contact': group.contact,
                           'phoneno': group.phoneno,
                           'address': group.address,
                           'is_favorite': is_favorite,
                           'is_enrolled': is_enrolled,
                           'enrolls': enrolls,
                           'comments': count,
                           'favorites': favorites,
                           'swipeshow_album': group.swipeshow_album.id,
                           'groups_album': group.groups_album.id,
                           'avg': avg
                     })
        except Exception, e:
            print e
            return self.error()

    def courses(self):
        inputs = self.getInput()
        is_star = int(inputs['is_star']) if inputs.has_key('is_star') else -1
        group = int(inputs['group']) if inputs.has_key('group') else 0
        page = int(inputs['page']) if inputs.has_key('page') else 0
        offset = int(inputs['offset']) if inputs.has_key('offset') else 0
        limit = int(inputs['limit']) if inputs.has_key('limit') else COUNT_PER_PAGE

        coursesList = Courses.select() 
        if is_star >= 0:
            coursesList = coursesList.where(Courses.is_star == is_star)
        elif group:
            coursesList = coursesList.where(Courses.group == group)

        if page:
            coursesList = coursesList.order_by(Courses.id.desc()).paginate(page, limit)
        elif offset:
            coursesList  = coursesList.where(Courses.id > offset).order_by(Courses.id.desc())

        return json.dumps([{
                        'name': course.name, 
                        'description': self.subText(self.htmlunquote(course.description), 0, 32), 
                        'thumbnail': course.thumbnail.thumbnail,
                        'id': course.id,
                        'price': course.price,
                        'discount': course.discount,
                        'category': course.category.name,
                        'group': course.group.name,
                    } for course in coursesList], cls = jsonEncoder)

    def courseinfo(self):
        inputs = self.getInput()
        is_favorite = False

        try:
            user = Users.get(Users.token == inputs['token'])
            favorite = CourseFavorites.get(
                CourseFavorites.owner == user,
                CourseFavorites.course == int(inputs['id'])
            )
            is_favorite = True            
        except Exception, e:
            pass

 
        try:
            course = Courses.get(Courses.id == (int(inputs['id'])))

            return json.dumps(
                     {
                        'name': course.name, 
                        'description': self.htmlunescape(course.description), 
                        'thumbnail': course.thumbnail.thumbnail,
                        'id': course.id,
                        'is_favorite': is_favorite,
                        'price': course.price,
                        'discount': course.discount,
                        'category': course.category.name,
                        'group': course.group.name,
                        'is_star': course.is_star,
                        'video_name': course.video_name,
                        'video_desc': course.video_desc,
                        'video_url': course.video_url,
                        'video_mobile_url': course.video_mobile_url,
                        'video_adaptive_url': course.video_mobile_url,
                        'video_rate': course.video_rate,
                        'video_width': course.video_width,
                        'video_height': course.video_height,
                        'video_thumbnail': course.video_thumbnail,
                        'video_uptime': course.video_uptime,
                        'video_duration': course.video_duration
                     })
        except Exception, e:
            return self.error()

    def agents(self):
        inputs = self.getInput()
        page = int(inputs['page']) if inputs.has_key('page') else 0
        offset = int(inputs['offset']) if inputs.has_key('offset') else 0
        limit = int(inputs['limit']) if inputs.has_key('limit') else COUNT_PER_PAGE

        agentsList = Agents.select()

        if page:
            agentsList = agentsList \
                                .order_by(Agents.id.desc()) \
                                .paginate(page, limit)
        elif offset:
            agentsList  = agentsList.where(Agents.id > offset) \
                                .order_by(Agents.id.desc())

        return json.dumps([
                    {
                        'id': agent.id,
                        'name': agent.name,
                        'thumbnail': agent.thumbnail.thumbnail,
                        'content': self.subText(self.htmlunquote(agent.content), 0, 32),
                    } for agent in agentsList])


    def agentinfo(self):
        inputs = self.getInput()

        try:
            agent = Agents.get(Agents.id == (int(inputs['id'])))

            return json.dumps(
                    {
                        'id': agent.id,
                        'name': agent.name,
                        'content': self.htmlunescape(agent.content)
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

    def favorite_courses(self):
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

            favsList = CourseFavorites.select().where(CourseFavorites.owner==user)
            if page:
                favsList = favsList \
                                .order_by(CourseFavorites.id.desc()) \
                                .paginate(page, limit)
            elif offset:
                favsList  = favsList.where(CourseFavorites.id > offset) \
                                .order_by(CourseFavorites.id.desc())

            return json.dumps([
                    {
                        'id': fav.id,
                        'user': user.id,
                        'course': fav.course.id,
                        'price': fav.course.price,
                        'name': fav.course.name,
                        'group_name': fav.course.group.name,
                        'created_time': fav.created_time,
                        'thumbnail': fav.course.thumbnail.thumbnail,
                        'category': fav.course.category.name,
                        'description': self.subText(self.htmlunquote(fav.course.description), 0, 32),
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
                        'price_home_service': fav.group.price_home_service,
                        'price_remote_service': fav.group.price_remote_service,
                        'description': self.subText(self.htmlunquote(fav.group.description), 0, 32),
                        'enrolls': GroupEnrollments.select().where(GroupEnrollments.group==fav.group).count(),
                        'favorites': GroupFavorites.select().where(GroupFavorites.group==fav.group).count(),
                        'comments': GroupComments.select().where(GroupComments.group==fav.group).count(),
                    } for fav in favsList], cls=jsonEncoder)
        except Exception, e:
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

    def like_course(self):
        inputs = self.getInput()

        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            course = inputs['course']
            fav = CourseFavorites.get_or_create(
                    owner=user, 
                    course=course,
                  )
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

    def course_comments(self):
        inputs = self.getInput()

        try:
            course = int(inputs['course'])
            page = int(inputs['page']) if inputs.has_key('page') else 0
            offset = int(inputs['offset']) if inputs.has_key('offset') else 0
            limit = int(inputs['limit']) if inputs.has_key('limit') else COUNT_PER_PAGE

            commentList = CourseComments.select().where(CourseComments.course==course)
            if page:
                commentList = commentList \
                                .order_by(CourseComments.id.desc()) \
                                .paginate(page, limit)
            elif offset:
                commentList  = commentList.where(CourseComments.id>offset) \
                                .order_by(CourseComments.id.desc())

            return json.dumps([
                    {
                        'id': comment.id,
                        'course': comment.course.id,
                        'user': comment.owner.name,
                        'created_time': str(comment.created_time)[:16],
                        'thumbnail': comment.owner.avatur,
                        'gender': comment.owner.gender,
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

    def comment_course(self):
        inputs = self.getInput()

        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            course = inputs['course']
            content = inputs['content']
            comment = CourseComments.get_or_create(
                    owner=user, 
                    course=course,
                    content=content,
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
            print e
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
                        'type': groupranking.type,
                    } for groupranking in rankingList], cls=jsonEncoder)
        except Exception, e:
            return self.error()

    def course_rankings(self):
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

            rankingList = CourseRankings.select().where(CourseRankings.owner==user)
            if page:
                rankingList = rankingList \
                                .order_by(CourseRankings.id.desc()) \
                                .paginate(page, limit)
            elif offset:
                rankingList  = rankingList.where(CourseRankings.id>offset) \
                                .order_by(CourseRankings.id.desc())

            return json.dumps([
                    {
                        'id': courseranking.id,
                        'user': user.id,
                        'created_time': courseranking.created_time,
                        'value': courseranking.value,
                        'course': courseranking.course.id,
                    } for courseranking in rankingList], cls=jsonEncoder)
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

    def rank_course(self):
        inputs = self.getInput()

        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            course = inputs['course']
            value = inputs['value']
            type = inputs['type']
            rankings = CourseRankings.get_or_create(
                    owner=user, 
                    value=value,
                    course=course,
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
                    description = self.subText(self.htmlunquote(group.description), 0, 32)
                except Exception, e:
                    try:
                        course = CoursePayments.get(CoursePayments.transaction==t).course
                        name = course.name
                        thumbnail = course.thumbnail.thumbnail
                        description = self.subText(self.htmlunquote(course.description), 0, 32)
                    except Exception, e:
                        continue
            
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
                        'courses': 
                            [{
                                'name': p.course.name,
                                'description': self.subText(self.htmlunquote(p.course.description), 0, 32),
                                'thumbnail': p.course.thumbnail.thumbnail,
                            } for p in t.course_payments_transaction],
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

    def enroll_group(self):
        inputs = self.getInput()

        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            group = inputs['group']            
            GroupEnrollments.get_or_create(
                    owner=user, 
                    group=group,
                  )
            return self.success()
        except Exception, e:
            return self.error()

    def enrollments(self):
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

            enrollmentsList = GroupEnrollments.select().where(GroupEnrollments.owner==user)
            if page:
                enrollmentsList = enrollmentsList \
                                .order_by(GroupEnrollments.id.desc()) \
                                .paginate(page, limit)
            elif offset:
                enrollmentsList  = enrollmentsList \
                                .where(GroupEnrollments.id > offset) \
                                .order_by(GroupEnrollments.id.desc())

            return json.dumps([
                    {
                        'id': enrollment.id,
                        'group': enrollment.group.id,
                        'name': enrollment.group.name,
                        'price_home_service': enrollment.group.price_home_service,
                        'price_remote_service': enrollment.group.price_remote_service,
                        'category': enrollment.group.category.name,
                        'description': self.subText(self.htmlunquote(enrollment.group.description), 0, 32),
                        'distance': distance_to_str(utils.distance(latitude, longitude, enrollment.group.latitude, enrollment.group.longitude)),
                        'specials': enrollment.group.specials,
                        'chatroom': enrollment.group.chatroom,
                        'chatroom_name': enrollment.group.chatroom_name,
                        'thumbnail': enrollment.group.thumbnail.thumbnail,
                        'enrolls': GroupEnrollments.select().where(GroupEnrollments.group==enrollment.group).count(),
                        'favorites': GroupFavorites.select().where(GroupFavorites.group==enrollment.group).count(),
                        'comments': GroupComments.select().where(GroupComments.group==enrollment.group).count(),
                    } for enrollment in enrollmentsList])
        except Exception, e:
            return self.error()  

    def quit_group(self):    
        inputs = self.getInput()
        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            enroll = GroupEnrollments.get(
                    owner=user, 
                    group=int(inputs['group']),
                  )
            enroll.delete_instance()
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


    def unlike_course(self):
        inputs = self.getInput()

        # 检查用户是否登录，否则返回403错误，前台需要切换到
        try:
            user = Users.get(Users.token == inputs['token'])
        except Exception, e:
            return self.forbidden()

        try:
            fav = CourseFavorites.get(
                    owner=user, 
                    course=int(inputs['course']),
                  )
            fav.delete_instance()
            return self.success()
        except Exception, e:
            return self.error()

    def comments(self):
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
                        'thumbnail': comment.owner.avatur,
                        'gender': comment.owner.gender,
                        'content': self.subText(self.htmlunquote(comment.content), 0, 64),
                    } for comment in commentList], cls=jsonEncoder)
        except Exception, e:
            return self.error()
    def total_comments(self,group_id):
        inputs = self.getInput()
        try:
            count = GroupComments.select().where(GroupComments.group==group_id).count()
            commentList = GroupComments.select().where(GroupComments.group==group_id)
            sum = 0
            for comment in commentList:
                sum += comment.value 
            avg = sum/count   
        except Exception, e:
            print e
            return self.error() 
