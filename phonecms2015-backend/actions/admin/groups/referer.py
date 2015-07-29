# -*- coding: utf-8 -*-
#coding=utf-8

import config
from actions.admin.base import adminAction
from models.categories import Categories
from models.images import Images
from models.albums import Albums
from models.users import Users
from models.groups import Groups
from models.group_comments import GroupComments
from models.group_favorites import GroupFavorites
from models.group_rankings import GroupRankings

'''
Admin controller: Group
'''
class refererAction(adminAction):
    def __init__(self):
        adminAction.__init__(self)

    def GET(self, name):
        if name == 'list':
            return self.list()
        elif name == 'add':
            return self.add()
        elif name == 'delete':
            return self.delete()
        elif name == 'commdelete':
            return self.commdelete()
        elif name == 'edit':
            return self.edit()
        elif name == 'comments':
            return self.comments()
        elif name == 'favorites':
            return self.favorite()
        elif name == 'favdelete':
            return self.favdelete()
        elif name == 'ranklist':
            return self.ranklist()
        elif name == 'rankdelete':
            return self.rankdelete()
        elif name == 'userslist':
            return self.userslist()

        return self.notFound()

    def POST(self, name):
        if name == 'save':
            return self.save()
        elif name == 'update':
            return self.update()
        elif name == 'commupdate':
            return self.commupdate()
        elif name == 'search':
            return self.search()
        elif name == 'search_by_category':
	        return self.search_by_category()

        return self.notFound()

    def list(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE
   
        groupsList = Groups.select()
        current_user = Users.get(Users.name == self.isLogin())
        if not self.isAdmin():
            groupsList = groupsList.where(Groups.owner == current_user)
        groupsList = groupsList.order_by(Groups.id.desc())
        pageString = self.getPageStr('/admin/groups/list', page, count, groupsList.count())
        self.privData['GROUPS_LIST'] = groupsList.paginate(page, count)
        self.privData['PAGE_STRING'] = pageString

        categoriesList = Categories().select()
        self.privData['CATEGORIES_LIST'] = categoriesList
        return self.display('groupsList')

    def search(self):
        inputParams = self.getInput()
        keywords = inputParams['keywords'].strip().lower() if inputParams.has_key('keywords') else ''

        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE

        groupsList = Groups.select().where(Groups.name.contains(keywords))
        current_user = Users.get(Users.name == self.isLogin())
        if not self.isAdmin():
            groupsList = groupsList.where(Groups.owner == current_user)

        pageString = self.getPageStr('/admin/groups/list', page, count, groupsList.count())
        self.privData['GROUPS_LIST'] = groupsList.order_by(Groups.id.desc()).paginate(page, page+count)
        self.privData['PAGE_STRING'] = pageString

        categoriesList = Categories().select()
        self.privData['CATEGORIES_LIST'] = categoriesList

        return self.display('groupsList')

    def search_by_category(self):
        inputParams = self.getInput()
        category = int(inputParams['category']) if inputParams.has_key('category') else 0
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE

        groupsList = Groups.select().where(Groups.category == category)
        current_user = Users.get(Users.name == self.isLogin())
        if not self.isAdmin():
            groupsList = groupsList.where(Groups.owner == current_user)

        pageString = self.getPageStr('/admin/groups/list', page, count, groupsList.count())
        self.privData['GROUPS_LIST'] = groupsList.order_by(Groups.id.desc()).paginate(page, page+count)
        self.privData['PAGE_STRING'] = pageString
        categoriesList = Categories().select()
        self.privData['CATEGORIES_LIST'] = categoriesList

        return self.display('groupsList')

        
    def delete(self):
        inputParams = self.getInput()
        group = Groups.get(Groups.id == int(inputParams['id']))

        current_user = Users.get(Users.name == self.isLogin())
        if current_user.id != group.owner.id and not self.isAdmin() or not current_user.role.type < 100:
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/groups/list'))

        try:
            group.delete_instance()
        except Exception, e:
            return self.success(msg='公司删除失败: %s' % e, url=self.makeUrl('/admin/groups/list'))

        return self.success(msg='公司删除成功', url=self.makeUrl('/admin/groups/list'))

    def edit(self):
        inputParams = self.getInput()
        groupID = inputParams['id']

        current_group = Groups().get(Groups.id == groupID)
        current_user = Users.get(Users.name == self.isLogin())

        if current_user.id != current_group.owner.id and not self.isAdmin() or not current_user.role.type < 100:
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/groups/list'))

        categoriesList = Categories().select()
        albumsList = Albums().select()
        imagesList = Images().select()
        if not self.isAdmin():
            albumsList = albumsList.where(Albums.owner == current_user)
            imagesList = imagesList.where(Images.owner == current_user)


        # 确认当前用户是否至少有一个包含图片的专辑
        if not albumsList.count():
            return self.error(msg = '请创建至少一个专辑!', url=self.makeUrl('/admin/albums/list'))
        if not imagesList.count(): 
            return self.error(msg = '请创建至少一个图片!', url=self.makeUrl('/admin/images/list'))

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
        self.privData['CATEGORIES_LIST'] = categoriesList
        self.privData['IMG_ALBUMS_LIST'] = album_images_map
        
        self.privData['CURRENT_OBJECT'] = current_group 
        self.privData['CURRENT_IMG'] = current_group.thumbnail
        self.privData['CURRENT_ALBUM'] = current_group.thumbnail.album
        self.privData['SUBMIT_NAME'] = "thumbnail"

        return self.display('groupEdit')

    def update(self):
        inputParams= self.getInput() 
        group = Groups.get(Groups.id == int(inputParams['id']))
 
        current_user = Users.get(Users.name == self.isLogin())
        if current_user.id != group.owner.id and not self.isAdmin() or not current_user.role.type < 100:
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/groups/list'))

        try:
            group.regions = inputParams['regions']
            group.name = inputParams['name']
            group.owner = current_user
            group.phoneno = inputParams['phoneno']
            group.cellphone = inputParams['cellphone']
            group.faxno = inputParams['faxno']
            group.postcode = inputParams['postcode']
            group.contact = inputParams['contact']
            group.description = self.htmlunquote(inputParams['description'])
            group.thumbnail = int(inputParams['thumbnail'])
            group.team_description = self.htmlunquote(inputParams['team_description'])
            group.regions = inputParams['regions']
            group.service_modes = inputParams['service_modes']
            group.specials = inputParams['specials']
            group.swipeshow_album = int(inputParams['swipeshow_album'])
            group.groups_album = int(inputParams['groups_album'])
            group.price1 = float(inputParams['price1'])
            group.price2 = float(inputParams['price2'])
            group.address = inputParams['address']
            group.longitude = float(inputParams['longitude'])
            group.latitude = float(inputParams['latitude'])
            group.category = int(inputParams['category'])
            group.save()
        except Exception, e:
            return self.error(msg = '公司修改失败: %s' % e, url=self.makeUrl('/admin/groups/list'))

        return self.success('公司修改成功!', url=self.makeUrl('/admin/groups/list'))

    def add(self):
        categoriesList = Categories().select()

        # 获得当前用户的专辑列表和图片列表
        albumsList = Albums().select() 
        imagesList = Images().select()
        current_user = Users.get(Users.name == self.isLogin())
        if not self.isAdmin():
            albumsList = albumsList.where(Albums.owner == current_user)
            imagesList = imagesList.where(Images.owner == current_user)
       
        if not current_user.role.type < 100:
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/albums/list'))

        # 确认当前用户是否至少有一个包含图片的专辑
        if not albumsList.count():
            return self.error(msg = '请创建至少一个专辑!', url=self.makeUrl('/admin/albums/list'))
        if not imagesList.count(): 
            return self.error(msg = '请创建至少一个图片!', url=self.makeUrl('/admin/images/list'))

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
        self.privData['CATEGORIES_LIST'] = categoriesList
        self.privData['IMG_ALBUMS_LIST'] = album_images_map
        
        # 默认专辑为当前用户的第一个专辑
        self.privData['CURRENT_ALBUM'] = self.privData['ALBUMS_LIST'][0]
        # 默认图片为默认专辑的第一张图片
        self.privData['CURRENT_IMG'] = album_images_map[self.privData['CURRENT_ALBUM'].id][0]
        self.privData['SUBMIT_NAME'] = "thumbnail"

        return self.display('groupAdd')


    def save(self):
        inputParams= self.getInput()

        try:
            current_user = Users.get(Users.name == self.isLogin())
            inputParams['longitude'] = inputParams['longitude'] if inputParams['longitude'] else 116.397428
            inputParams['latitude'] = inputParams['latitude'] if inputParams['latitude'] else 39.90923

            Groups.create(
                name = inputParams['name'],
                owner = current_user,
                address = inputParams['address'],
                phoneno = inputParams['phoneno'],
                cellphone = inputParams['cellphone'],
                faxno = inputParams['faxno'],
                postcode = inputParams['postcode'],
                contact = inputParams['contact'],
                description = self.htmlunquote(inputParams['description']),
                thumbnail = int(inputParams['thumbnail']), 
                team_description = self.htmlunquote(inputParams['team_description']),
                regions = inputParams['regions'],
                service_modes = inputParams['service_modes'],
                specials = inputParams['specials'],
                swipeshow_album = int(inputParams['swipeshow_album']),
                groups_album = int(inputParams['groups_album']),
                price1 = float(inputParams['price1']),
                price2 = float(inputParams['price2']),
                longitude = float(inputParams['longitude']),
                latitude = float(inputParams['latitude']),
                category = int(inputParams['category']),
            )  
        except Exception, e:
            return self.error(msg = '新增公司失败: %s' % e, url=self.makeUrl('/admin/groups/list'))

        return self.success('新增公司成功', url=self.makeUrl('/admin/groups/list'))

    def ranklist(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE
###打分是都能看到
        groupRankList = GroupRankings.select().order_by(GroupRankings.id.desc())
        pageString = self.getPageStr('/admin/groups/ranklist', page, count, groupRankList.count())
        self.privData['GROUPRANK_LIST'] = groupRankList.paginate(page, count)
        self.privData['PAGE_STRING'] = pageString

        return self.display('grouprankViewList')

    def rankdelete(self):
        inputParams = self.getInput()
        grouprank = GroupRankings.get(GroupRankings.id == int(inputParams['id']))

        current_user = Users.get(Users.name == self.isLogin())
        if current_user.id != grouprank.owner.id and not self.isAdmin() or not current_user.role.type < 100:
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/groups/ranklist'))

        try:
            grouprank.delete_instance()
        except Exception, e:
            return self.success(msg='公司评价删除失败: %s' % e, url=self.makeUrl('/admin/groups/ranklist'))

        return self.success(msg='公司评价删除成功', url=self.makeUrl('/admin/groups/ranklist'))



    def comments(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE
###评论是都能看到
        groupCommentList = GroupComments.select()
        pageString = self.getPageStr('/admin/groups/comments', page, count, groupCommentList.count())
        self.privData['GROUPCOMM_LIST'] = groupCommentList.order_by(GroupComments.id.desc()).paginate(page, count)
        self.privData['PAGE_STRING'] = pageString

        return self.display('groupcommViewList')


    def commupdate(self):
        inputParams= self.getInput()
        groupcomm = GroupComments.get(GroupComments.id == int(inputParams['id']))

        current_user = Users.get(Users.name == self.isLogin())
        if current_user.id != groupcomm.owner.id and not self.isAdmin() or  not current_user.role.type < 100:
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/groups/list'))

        try:
            groupcomm.content = inputParams['content']
            ##现在时间没有更新，需要更新时间为当前时间
            groupcomm.save()
        except Exception, e:
            return self.error(msg = '公司评论修改失败: %s' % e, url=self.makeUrl('/admin/groups/comments'))

        return self.success('公司评论修改成功!', url=self.makeUrl('/admin/groups/comments'))

    def commdelete(self):
        inputParams = self.getInput()
        groupcomm = GroupComments.get(GroupComments.id == int(inputParams['id']))

        current_user = Users.get(Users.name == self.isLogin())
        if current_user.id != groupcomm.owner.id and not self.isAdmin() or not current_user.role.type < 100:
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/groups/comments'))

        try:
            groupcomm.delete_instance()
        except Exception, e:
            return self.success(msg='公司评论删除失败: %s' % e, url=self.makeUrl('/admin/groups/comments'))

        return self.success(msg='公司评论删除成功', url=self.makeUrl('/admin/groups/comments'))

    def favorite(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE
        ###favotar只有admin能看到全部的，否则只能看到本人的
        current_user = Users.get(Users.name == self.isLogin())
        groupFavList = GroupFavorites.select()
        if not self.isAdmin():
            groupFavList = groupFavList.where(GroupFavorites.owner == current_user.id)
        pageString = self.getPageStr('/admin/groups/favorite', page, count, groupFavList.count())
        self.privData['GROUPFAV_LIST'] = groupFavList.order_by(GroupFavorites.id.desc()).paginate(page, count)
        self.privData['PAGE_STRING'] = pageString

        return self.display('groupfavViewList')

    def favdelete(self):
        inputParams = self.getInput()
        groupfav = GroupFavorites.get(GroupFavorites.id == int(inputParams['id']))

        current_user = Users.get(Users.name == self.isLogin())
        if current_user.id != groupfav.owner.id and not self.isAdmin() or  not current_user.role.type < 100:
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/groups/favorites'))

        try:
            groupfav.delete_instance()
        except Exception, e:
            return self.success(msg='公司收藏删除失败: %s' % e, url=self.makeUrl('/admin/groups/favorites'))

        return self.success(msg='公司收藏删除成功', url=self.makeUrl('/admin/groups/favorites'))


