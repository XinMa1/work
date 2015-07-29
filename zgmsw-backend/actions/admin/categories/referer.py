# -*- coding: utf-8 -*-
#coding=utf-8

import config
from actions.admin.base import adminAction
from models.categories import Categories
from models.categories import Categories
from models.images import Images
from models.albums import Albums

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

        categoriesList = Categories.select().order_by(Categories.id.desc())

        pageString = self.getPageStr(self.makeUrl('/admin/categories/list'), page, count, categoriesList.count())
        self.privData['CATEGORIES_LIST'] = categoriesList.paginate(page, count)
        self.privData['PAGE_STRING'] = pageString


        return self.display('categoriesList')

    def delete(self):
        inputParams = self.getInput()

        try:
            if int(inputParams['id']) == 1:
                return self.error(msg='不能删除系统预置分类', url=self.makeUrl('/admin/categories/list'))
           
            if  not self.isAdmin():
                return self.error(msg = '权限不足!', url=self.makeUrl('/admin/categories/list')) 
            category = Categories.get(Categories.id == int(inputParams['id']))
            category.delete_instance()
        except Exception, e:
            return self.error(msg = '分类删除失败: %s' % e, url=self.makeUrl('/admin/categories/list'))
    
        return self.success(msg='分类删除成功', url=self.makeUrl('/admin/categories/list'))

     
    def search(self):
        inputParams = self.getInput()
        keywords = inputParams['keywords'].strip().lower() if inputParams.has_key('keywords') else ''
        
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE

        categoriesList = Categories().select().where(Categories.name.contains(keywords))

        categoryName = {}
        for category in categoriesList:
            categoryName[category.id] = category.name

        pageString = self.getPageStr(self.makeUrl('/admin/categories/list'), page, count, categoriesList.count())
        self.privData['CATEGORIES_LIST'] = categoriesList.paginate(page, count)
        self.privData['PAGE_STRING'] = pageString

        return self.display('categoriesList')

        
    def add(self):
        if  not self.isAdmin():
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/categories/list'))

        self.privData['ENABLE_SELECT_THUMBNAIL'] = False
        self.privData['CATEGORIES_LIST'] = Categories.select()

        imagesList = Images().select()
        albumsList = Albums().select()

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
 
        return self.display('categoryAdd')

    def modify(self):
        inputParams = self.getInput()
        if not self.isAdmin():
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/categories/list'))

        category_id = int(inputParams['id'])
        if category_id  == 1:
            return self.error(msg='不能编辑系统预置分类', url=self.makeUrl('/admin/categories/list'))

        thumbnail_id = int(inputParams['thumbnail']) if inputParams.has_key('thumbnail') else 0
        if thumbnail_id:
            thumbnail_data = Images.get(Images.id == thumbnail_id).thumbnail
        else:
            import base64
            from imaging import imaging
            thumbnail_data = base64.b64encode(buffer(imaging.default_thumbnail()))

        try:
            category = Categories().get(Categories.id == category_id)
           
            category.name = inputParams['name']
            category.description = inputParams['desc']
            category.parent = int(inputParams['parent'])
            category.thumbnail = thumbnail_data 
            category.save()
        except Exception, e:
            return self.error(msg = '分类修改失败: %s' % e, url=self.makeUrl('/admin/categories/list'))

        return self.success('分类修改成功', url=self.makeUrl('/admin/categories/list'))

    def edit(self):
        inputParams = self.getInput()
        if not self.isAdmin():
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/categories/list'))

        categoryID = int(inputParams['id'])
        if categoryID  == 1:
            return self.error(msg='不能编辑系统预置分类', url=self.makeUrl('/admin/categories/list'))
        categoriesObj = Categories.get(Categories.id == categoryID)
        self.privData['CATEGORY'] =  categoriesObj
        self.privData['CATEGORIES_LIST'] = Categories.select()
        self.privData['ENABLE_SELECT_THUMBNAIL'] = False

        imagesList = Images().select()
        albumsList = Albums().select()

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
 
        return self.display('categoryEdit')


    def save(self):
        userInput = self.getInput()  
        if not self.isAdmin():
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/categories/list'))

        thumbnail_id = int(userInput['thumbnail']) if userInput.has_key('thumbnail') else 0
        if thumbnail_id:
            thumbnail_data = Images.get(Images.id == thumbnail_id).thumbnail
        else:
            import base64
            from imaging import imaging
            thumbnail_data = base64.b64encode(buffer(imaging.default_thumbnail()))

        try:
            Categories.create(
                name = userInput['name'],
                description = userInput['desc'],
                thumbnail = thumbnail_data,
                parent = int(userInput['parent'])
            )
          
        except Exception, e:
            return self.error(msg = '新增分类失败: %s' % e, url=self.makeUrl('/admin/categories/list'))

        return self.success('新增分类成功', url=self.makeUrl('/admin/categories/list'))
