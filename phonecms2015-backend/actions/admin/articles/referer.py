# -*- coding: utf-8 -*-
#coding=utf-8

import config
from actions.admin.base import adminAction
from models.articles import Articles
from models.images import Images
from models.albums import Albums
from models.users import Users
from models.categories import Categories
from models.article_favorites import ArticleFavorites

'''
Admin controller: categories administration views.
'''
class refererAction(adminAction):
    def __init__(self):
        adminAction.__init__(self)

    def GET(self, name):
        if name == 'list':
            return self.list()
        elif name == 'delete':
            return self.delete()
        elif name == 'add':
            return self.add()
        elif name == 'edit':
            return self.edit()
        elif name == 'favorites':
            return self.favorite()
        elif name == 'favdelete':
            return self.favdelete()
        else:
            return self.notFound()

    def POST(self, name):
        if name == 'save':
            return self.save()
        elif name == 'search':
            return self.search() 
        elif name == 'modify':
            return self.modify()
        else:
            return self.notFound()

    def list(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE

        articlesList = Articles.select()

        pageString = self.getPageStr(self.makeUrl('/admin/articles/list'), page, count, articlesList.count())
        articlesList = articlesList.order_by(Articles.id.desc())
        self.privData['ARTICLES_LIST'] = articlesList.paginate(page, page+count)
        self.privData['PAGE_STRING'] = pageString
        self.privData['ARTICLES_LIST'] = articlesList

        return self.display('articlesList')

    def delete(self):
        inputParams = self.getInput()

        try:
            current_user = Users.get(Users.name == self.isLogin())
            if  not self.isAdmin():
                return self.error(msg = '权限不足!', url=self.makeUrl('/admin/articles/list')) 
            article = Articles.get(Articles.id == int(inputParams['id']))
            article.delete_instance()
        except Exception, e:
            return self.error(msg = '删除文章失败: %s' % e, url=self.makeUrl('/admin/articles/list'))
    
        return self.success(msg='删除文章成功', url=self.makeUrl('/admin/articles/list'))

     
    def search(self):
        inputParams = self.getInput()
        keywords = inputParams['keywords'].strip().lower() if inputParams.has_key('keywords') else ''
        
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE

        articlesList = Articles.select().where(Articles.name.contains(keywords))
        pageString = self.getPageStr(self.makeUrl('/admin/articles/list'), page, count, articlesList.count())
        articlesList = articlesList.order_by(Articles.id.desc())
        self.privData['ARTICLES_LIST'] = articlesList.paginate(page, page+count)
        self.privData['PAGE_STRING'] = pageString
        self.privData['ARTICLES_LIST'] = articlesList
        return self.display('articlesList')

        
    def add(self):
        articlesList = Articles().select()

        userName = self.isLogin()
        if userName != 'admin':
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/articles/list'))
        user = Users.get(Users.name == userName)
        albumsList = Albums().select().where(Albums.owner == user.id)
        imagesList = Images().select().where(Images.owner == user.id)
        categoriesList = Categories().select()

        if not albumsList.count():
            return self.error(msg = '请创建至少一个专辑!', url=self.makeUrl('/admin/articles/list'))
        if not imagesList.count():
            return self.error(msg = '请创建至少一个图片!', url=self.makeUrl('/admin/articles/list'))

        album_images_map = {}
        excluded_albums = []
        for album in albumsList:
            album_images = imagesList.where(Images.album == album.id)
            if album_images.count():
                album_images_map[album.id] = album_images
            else:
                excluded_albums.append(album.id)

        # 分类列表
        self.privData['CATEGORIES_LIST'] = categoriesList

        self.privData['ALBUMS_LIST'] = \
            [album for album in albumsList if album.id not in excluded_albums]
        self.privData['IMG_ALBUMS_LIST'] = album_images_map

        # 默认专辑为当前用户的第一个专辑
        self.privData['CURRENT_ALBUM'] = self.privData['ALBUMS_LIST'][0]
        # 默认图片为默认专辑的第一张图片
        self.privData['CURRENT_IMG'] = album_images_map[self.privData['CURRENT_ALBUM'].id][0]
        self.privData['SUBMIT_NAME'] = "thumbnail"

        return self.display('articleAdd')

    def modify(self):
        inputParams= self.getInput()
         
        try:
            print inputParams['category']
            print inputParams['id']
            articleId = int(inputParams['id'])
            q = Articles.update(
                category = int(inputParams['category']),
                name = inputParams['name'],
                content = inputParams['content'],
                thumbnail = int(inputParams['thumbnail']),
            ).where(Articles.id == articleId)
            q.execute()
        except Exception, e:
            return self.error(msg = '文章修改失败: %s' % e, url=self.makeUrl('/admin/articles/list'))

        return self.success('文章修改成功', url=self.makeUrl('/admin/articles/list'))

    def edit(self):
        inputParams = self.getInput()
        userName = self.isLogin()
        if userName != 'admin':
            return self.error(msg = '权限不足!',url=self.makeUrl('/admin/articles/list'))

        articleID = int(inputParams['id'])
        article = Articles.get(Articles.id == articleID)

        self.privData['ARTICLE'] = article

        user = Users.get(Users.name == userName)
        albumsList = Albums().select().where(Albums.owner == user.id)
        imagesList = Images().select().where(Images.owner == user.id)
        categoriesList = Categories().select()

        # 确认当前用户是否至少有一个包含图片的专辑
        if not albumsList.count():
            return self.error(msg = '请创建至少一个专辑!', url=self.makeUrl('/admin/albums/list'))
        if not imagesList.count():
            return self.error(msg = '请创建至少一个图片!', url=self.makeUrl('/admin/images/list'))

        # 分类列表
        self.privData['CATEGORIES_LIST'] = categoriesList

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

        self.privData['CURRENT_ARTICLE'] = article
        self.privData['CURRENT_ALBUM'] = article.thumbnail.album
        self.privData['CURRENT_IMG'] = article.thumbnail
        self.privData['SUBMIT_NAME'] = "thumbnail"

        return self.display('articleEdit')


    def save(self):
        userInput = self.getInput()  
        try:
            if not self.isAdmin():
                return self.error(msg = '权限不足!', url=self.makeUrl('/admin/articles/list'))

            thumbnail = int(userInput['thumbnail']);
            Articles.create(
                category = int(userInput['category']),
                name = userInput['name'],
                thumbnail = thumbnail,
                content = userInput['content']
            )
          
        except Exception, e:
            return self.error(msg = '新增文章失败: %s' % e, url=self.makeUrl('/admin/articles/list'))

        return self.success('新增文章成功', url=self.makeUrl('/admin/articles/list'))

    def favorite(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE
###favotar只有admin能看到全部的，否则只能看到本人的
        current_user = Users.get(Users.name == self.isLogin())
        articleFavList = ArticleFavorites.select()
        if not self.isAdmin():
            articleFavList = articleFavList.where(ArticleFavorites.owner == current_user.id)
        pageString = self.getPageStr('/admin/articles/favorites', page, count, articleFavList.count())
        self.privData['ARTICLEFAV_LIST'] = articleFavList.paginate(page, config.COUNT_PER_PAGE)
        self.privData['PAGE_STRING'] = pageString

        return self.display('articlefavViewList')

    def favdelete(self):
        inputParams = self.getInput()
        articlefav = ArticleFavorites.get(ArticleFavorites.id == int(inputParams['id']))

        current_user = Users.get(Users.name == self.isLogin())
        if current_user.id != articlefav.owner.id and not self.isAdmin() or not current_user.role.type < 100:
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/articles/favorites'))

        try:
            articlefav.delete_instance()
        except Exception, e:
            return self.success(msg='文章收藏删除失败: %s' % e, url=self.makeUrl('/admin/articles/favorites'))

        return self.success(msg='文章收藏删除成功', url=self.makeUrl('/admin/articles/favorites'))


