# -*- coding: utf-8 -*-
#coding=utf-8

import config
from actions.admin.base import adminAction
from models.courses import Courses
from models.categories import Categories
from models.images import Images
from models.albums import Albums
from models.users import Users
from models.groups import Groups
from models.course_comments import CourseComments
from models.course_favorites import CourseFavorites
from models.course_rankings import CourseRankings
'''
Admin controller: producing product administration views.
'''
class refererAction(adminAction):
    def __init__(self, name = '产品管理'):
        adminAction.__init__(self, name)

    def GET(self, name):
        if name == 'list':
            return self.list()
        elif name == 'add':
            return self.add()
        elif name == 'delete':
            return self.delete()
        elif name == 'listForBatchDel':
            return self.listForBatchDel()
        elif name == 'edit':
            return self.edit()
        elif name == 'map':
            return self.map()
        elif name == 'comments':
            return self.comments()
        elif name == 'commdelete':
            return self.commdelete()
        elif name == 'favorates':
            return self.favorate()
        elif name == 'favdelete':
            return self.favdelete()
        elif name == 'ranklist':
            return self.ranklist()
        elif name == 'rankdelete':
            return self.rankdelete()
        elif name == 'videos':
            return self.videos()
        else:
            return self.notFound()

    def POST(self, name):
        if name == 'save':
            return self.save()
        elif name == 'update':
            return self.update()
        elif name == 'search':
            return self.search()
        elif name == 'searchbycategory':
	    return self.searchbycategory()
        elif name == 'deleteBatch':
            return self.deleteBatch()
        elif name == 'commupdate':
            return self.commupdate()
        elif name == 'link':
            return self.link()

        return self.notFound()

    def list(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE
        categoriesList = Categories.select()
        coursesList = Courses.select()

        current_user = Users.get(Users.name == self.isLogin())
        if not self.isAdmin():
            coursesList = coursesList.where(Courses.owner == current_user)

        coursesList = coursesList.order_by(Courses.id.desc()) 
        pageString = self.getPageStr('/admin/courses/list', page, count, coursesList.count())
        self.privData['COURSES_LIST'] = coursesList.paginate(page, page+count)
        self.privData['PAGE_STRING'] = pageString
        self.privData['CATEGORIES_LIST'] = categoriesList
        return self.display('coursesList')

    def search(self):
        inputParams = self.getInput()
        keywords = inputParams['keywords'].strip().lower() if inputParams.has_key('keywords') else ''

        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE
        categoriesList = Categories.select()
        coursesList = Courses.select().where(Courses.name.contains(keywords))

        current_user = Users.get(Users.name == self.isLogin())
        if not self.isAdmin():
            coursesList = coursesList.where(Courses.owner == current_user)

        coursesList = coursesList.order_by(Courses.id.desc())
        pageString = self.getPageStr('/admin/courses/list', page, count, coursesList.count())
        self.privData['COURSES_LIST'] = coursesList.paginate(page, page+count)
        self.privData['PAGE_STRING'] = pageString
        self.privData['CATEGORIES_LIST'] = categoriesList
        return self.display('coursesList')
 

    def searchbycategory(self):
        inputParams = self.getInput()
        categoryName = inputParams['categoryselect'].strip().lower() if inputParams.has_key('categoryselect') else ''
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE

        categoriesList = Categories.select()
        coursesList = Courses.select().where(Courses.category == categoryName)
        current_user = Users.get(Users.name == self.isLogin())
        if not self.isAdmin():
            coursesList = coursesList.where(Courses.owner == current_user)

        coursesList = coursesList.order_by(Courses.id.desc()) 
        pageString = self.getPageStr('/admin/courses/list', page, count, coursesList.count())
        self.privData['COURSES_LIST'] = coursesList.paginate(page, page+count)
        self.privData['PAGE_STRING'] = pageString
        self.privData['CATEGORIES_LIST'] = categoriesList
        return self.display('coursesList')

        
    def delete(self):
        inputParams = self.getInput()
        try:
            courseID = inputParams['id']
            course = Courses.get(Courses.id == courseID)
            course.delete_instance()
        except Exception, e:
            return self.success(msg='课程删除失败: %s' % e, url=self.makeUrl('/admin/courses/list'))

        return self.success(msg='课程删除成功', url=self.makeUrl('/admin/courses/list'))

    def deleteBatch(self):
        inputParams = self.getInput()
        try:
            condition = ' id IN (' + inputParams['delitems'] +')'
            product().delete(condition)
        except Exception, e:
            return self.error(msg='对象删除失败: %s' % e, url=self.makeUrl('/admin/product/list'))

        return self.success(msg='对象删除成功', url=self.makeUrl('/admin/product/list'))

    def edit(self):
        inputParams = self.getInput()
        courseID = int(inputParams['id'])
        course = Courses.get(Courses.id == courseID)
        userName = self.isLogin()

        self.privData['COURSE'] =   course
        categoriesList = Categories.select()
        self.privData['CATEGORIES_LIST'] = categoriesList

        star_list = {'True':'是','False':'否'}
        self.privData['ISSTAR_LIST'] = star_list
        user = Users.get(Users.name == userName)
        if user != course.owner and not self.isAdmin() or not user.role.type < 100:
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/courses/list'))

        groupsList = Groups().select().where(Groups.owner == user.id)
        self.privData['GROUPS_LIST'] = groupsList
        albumsList = Albums().select().where(Albums.owner == user.id)
        imagesList = Images().select().where(Images.owner == user.id)

                # 确认当前用户是否至少有一个包含图片的专辑
        if not albumsList.count():
            return self.error(msg = '请创建至少一个专辑!', url=self.makeUrl('/admin/courses/list'))
        if not imagesList.count():
            return self.error(msg = '请创建至少一个图片!', url=self.makeUrl('/admin/courses/list'))

        # 构建{album: images}, 同时排除不包括任何图片的专辑
        album_images_map = {}
        excluded_albums = []
        for album in albumsList:
            album_images = imagesList.where(Images.album == album.id)
            if album_images.count():
                album_images_map[album.id] = album_images
            else:
                excluded_albums.append(album.id)

        self.privData['ALBUMS_LIST'] = \
            [album for album in albumsList if album.id not in excluded_albums]
        self.privData['IMG_ALBUMS_LIST'] = album_images_map

        self.privData['CURRENT_COURSE'] = course
        self.privData['CURRENT_ALBUM'] = course.thumbnail.album
        self.privData['CURRENT_IMG'] = course.thumbnail
        self.privData['SUBMIT_NAME'] = "thumbnail"

        return self.display('courseEdit')

    def update(self):
        inputParams= self.getInput()  
        courseId = inputParams['id']
        try:
            price = float(inputParams['price'])
            discount = float(inputParams['discount'])
        except ValueError as ve:
            return self.error(msg = '产品修改失败: 价格或折扣格式有误，需要是数字', url=self.makeUrl('/admin/product/list'))

        is_star = str(inputParams['star'])
        is_star = 0 if is_star == 'False' else 1


        try:
            course = Courses.get(Courses.id == courseId)
            current_user = Users.get(Users.name == self.isLogin())
            if current_user.id != course.owner.id and not self.isAdmin() or not current_user.role.type < 100:
                return self.error(msg = '权限不足!', url=self.makeUrl('/admin/courses/list'))

            q = Courses.update(price = price,discount= discount,is_star=is_star,description = self.htmlunquote(inputParams['desc']),thumbnail = int(inputParams['thumbnail']),video_url=inputParams['vedio_url'],group=int(inputParams['group']),category=int(inputParams['category']),name=inputParams['name']).where(Courses.id == courseId)
            q.execute()
        except Exception, e:
            return self.error(msg = '课程编辑失败: %s' % e, url=self.makeUrl('/admin/courses/list'))

        return self.success('课程编辑成功', url=self.makeUrl('/admin/courses/list'))

    def map(self):
        return self.display('map_select_widget')


    def add(self):

        userName = self.isLogin()
        user = Users.get(Users.name == userName)
        if not user.role.type < 100:
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/courses/list'))

        categoriesList = Categories.select()
        self.privData['CATEGORIES_LIST'] = categoriesList

        albumsList = Albums().select().where(Albums.owner == user.id)
        self.privData['ALBUMS_LIST'] = albumsList
        imagesList = Images().select().where(Images.owner == user.id)


        self.privData['USER'] = user
       
        groupsList = Groups().select().where(Groups.owner == user.id)
        #先创建一个班级，如果不存在班级，则需要先创建班级
        if not groupsList.count():
            return self.error(msg = '请先创建一个班级!', url=self.makeUrl('/admin/courses/list'))
        self.privData['GROUPS_LIST'] = groupsList

        # 构建{album: images}, 同时排除不包括任何图片的专辑
        album_images_map = {}
        excluded_albums = []
        for album in albumsList:
            album_images = imagesList.where(Images.album == album.id)
            if album_images.count():
                album_images_map[album.id] = album_images
            else:
                excluded_albums.append(album.id)

        if imagesList.count():
            self.privData['ENABLE_SELECT_THUMBNAIL'] = True
            self.privData['ALBUMS_LIST'] = \
                [album for album in albumsList if album.id not in excluded_albums]
            self.privData['IMG_ALBUMS_LIST'] = album_images_map
            self.privData['CURRENT_ALBUM'] = self.privData['ALBUMS_LIST'][0]
            # 默认图片为默认专辑的第一张图片
            self.privData['CURRENT_IMG'] = album_images_map[self.privData['CURRENT_ALBUM'].id][0]
            self.privData['SUBMIT_NAME'] = "thumbnail"

        return self.display('courseAdd')


    def save(self):
        inputParams= self.getInput()
        userName = self.isLogin()
        user = Users.get(Users.name == userName)

        thumbnail = int(inputParams['thumbnail']);
        try:
            try:
                price = float(inputParams['price'])
                discount = float(inputParams['discount'])
            except ValueError as ve:
                raise Exception("价格或折扣格式有误，需要是数字")
            Courses.create(
                name = inputParams['name'],
                price = price,
                discount = discount,
                is_star = int(inputParams['star']),
                description = self.htmlunquote(inputParams['desc']),
                owner = user.id,
                video_url = inputParams['vedio_url'],
                category = int(inputParams['category']),
                group = int(inputParams['group']),
                thumbnail = int(thumbnail)
            )

        except Exception, e:
            return self.error(msg = '新增课程失败: %s' % e, url=self.makeUrl('/admin/courses/list'))

        return self.success('新增课程成功', url=self.makeUrl('/admin/courses/list'))


    def comments(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE
###评论是都能看到
        courseCommentList = CourseComments.select()
        pageString = self.getPageStr('/admin/courses/comments', page, count, courseCommentList.count())
        self.privData['COURSECOMM_LIST'] = courseCommentList.paginate(page, config.COUNT_PER_PAGE)
        self.privData['PAGE_STRING'] = pageString

        return self.display('coursecommViewList')


    def commupdate(self):
        inputParams= self.getInput()
        coursecomm = CourseComments.get(CourseComments.id == int(inputParams['id']))

        current_user = Users.get(Users.name == self.isLogin())
        if current_user.id != coursecomm.owner.id and not self.isAdmin():
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/courses/list'))

        try:
            coursecomm.content = inputParams['content']
            ##现在时间没有更新，需要更新时间为当前时间
            coursecomm.save()
        except Exception, e:
            return self.error(msg = '课程评论修改失败: %s' % e, url=self.makeUrl('/admin/courses/comments'))

        return self.success('课程评论修改成功!', url=self.makeUrl('/admin/courses/comments'))

    def commdelete(self):
        import pdb;pdb.set_trace()
        inputParams = self.getInput()
        coursecomm = CourseComments.get(CourseComments.id == int(inputParams['id']))
        

        current_user = Users.get(Users.name == self.isLogin())
        if current_user.id != coursecomm.owner.id and not self.isAdmin() or not current_user.role.type < 100:
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/courses/comments'))

        try:
            coursecomm.delete_instance()
        except Exception, e:
            return self.success(msg='课程评论删除失败: %s' % e, url=self.makeUrl('/admin/courses/comments'))

        return self.success(msg='课程评论删除成功', url=self.makeUrl('/admin/courses/comments'))

    def favorate(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE
###favotar只有admin能看到全部的，否则只能看到本人的
        current_user = Users.get(Users.name == self.isLogin())
        courseFavList = CourseFavorites.select()
        if not self.isAdmin():
            courseFavList = courseFavList.where(CourseFavorites.owner == current_user.id)
        pageString = self.getPageStr('/admin/courses/favorates', page, count, courseFavList.count())
        self.privData['COURSEFAV_LIST'] = courseFavList.paginate(page, config.COUNT_PER_PAGE)
        self.privData['PAGE_STRING'] = pageString

        return self.display('coursefavViewList')

    def favdelete(self):
        inputParams = self.getInput()
        coursefav = CourseFavorites.get(CourseFavorites.id == int(inputParams['id']))

        current_user = Users.get(Users.name == self.isLogin())
        if current_user.id != coursefav.owner.id and not self.isAdmin() or not current_user.role.type < 100:
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/courses/favorates'))

        try:
            coursefav.delete_instance()
        except Exception, e:
            return self.success(msg='课程收藏删除失败: %s' % e, url=self.makeUrl('/admin/courses/favorates'))

        return self.success(msg='课程收藏删除成功', url=self.makeUrl('/admin/courses/favorates'))

    def ranklist(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE
###打分是都能看到
        courseRankList = CourseRankings.select().order_by(CourseRankings.id.desc())
        pageString = self.getPageStr('/admin/courses/ranklist', page, count, courseRankList.count())
        self.privData['COURSERANK_LIST'] = courseRankList.paginate(page, config.COUNT_PER_PAGE)
        self.privData['PAGE_STRING'] = pageString

        return self.display('courserankViewList')

    def rankdelete(self):
        inputParams = self.getInput()
        courserank = CourseRankings.get(CourseRankings.id == int(inputParams['id']))

        current_user = Users.get(Users.name == self.isLogin())
        if current_user.id != courserank.owner.id and not self.isAdmin() or not current_user.role.type < 100:
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/courses/ranklist'))

        try:
            courserank.delete_instance()
        except Exception, e:
            return self.error(msg='课程评价删除失败: %s' % e, url=self.makeUrl('/admin/courses/ranklist'))

        return self.success(msg='班级课程评价删除成功', url=self.makeUrl('/admin/courses/ranklist'))

    def videos(self):
        inputParams = self.getInput()

        try:
            import aodianyun
            courseId = int(inputParams['id'])

            course = Courses.get(Courses.id == courseId)
            current_user = Users.get(Users.name == self.isLogin())
            if current_user.id != course.owner.id and not self.isAdmin() or not current_user.role.type < 100:
                return self.error(msg = '权限不足!', url=self.makeUrl('/admin/courses/list'))
        
            vods = aodianyun.Apis().get_upload_vod_list()
            self.privData['VIDEOS_LIST'] = vods['List']
            self.privData['COURSE'] = course
            return self.display('courseLink')
        except Exception, e:
            return self.error(msg='关联视频失败: %s' % e, url=self.makeUrl('/admin/courses/list'))

    def link(self):
        inputParams= self.getInput()  
        courseId = inputParams['id']
        videoId = inputParams['sel']

        try:
            course = Courses.get(Courses.id == courseId)
            current_user = Users.get(Users.name == self.isLogin())
            if current_user.id != course.owner.id and not self.isAdmin() or not current_user.role.type < 100:
                return self.error(msg = '权限不足!', url=self.makeUrl('/admin/courses/list'))

            import aodianyun
            vods = aodianyun.Apis().get_upload_vod_list()['List']
            for vod in vods:
                if vod['id'] == videoId:
                    if vod.has_key('url'):
                        course.video_url=vod['url']
                    if vod.has_key('title'):
                        course.video_name=vod['title']
                    if vod.has_key('desc'):
                        course.video_desc=vod['desc']
                    if vod.has_key('m3u8_240'):
                        course.video_mobile_url=vod['m3u8_240']
                    if vod.has_key('adaptive'):
                        course.video_adaptive_url=vod['adaptive']
                    if vod.has_key('videoRate'):
                        course.video_rate=vod['videoRate']
                    if vod.has_key('width'):
                        course.video_width=vod['width']
                    if vod.has_key('height'):
                        course.video_height=vod['height']
                    if vod.has_key('thumbnail'):
                        course.video_thumbnail=vod['thumbnail']
                    if vod.has_key('uptime'):
                        course.video_uptime=vod['uptime']
                    if vod.has_key('duration'):
                        course.video_duration=vod['duration']
                    course.save()
        except Exception, e:
            return self.error(msg='关联视频失败: %s' % e, url=self.makeUrl('/admin/courses/list'))

        return self.success('关联视频成功', url=self.makeUrl('/admin/courses/list'))

 
