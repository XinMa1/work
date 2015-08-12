# -*- coding: utf-8 -*-
#coding=utf-8

import web
import os
import json
import config
from actions.admin.base import adminAction
from models.images import Images
from models.albums import Albums
from models.users import Users

'''
Admin controller: producing image administration views.
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
        elif name == 'thumbnail':
            return self.thumbnail()
        elif name == 'ajaximages':
            return self.getImages()
        else:
            return self.notFound()

    def POST(self, name):
        if name == 'save':
            return self.save()
        elif name == 'search':
            return self.search()
        elif name == 'search_by_album':
            return self.search_by_album()
        else:
            return self.notFound()

    def list(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1

        imgsList = Images.select()
        albumsList = Albums().select()
        current_user = Users.get(Users.name == self.isLogin())
        if not self.isAdmin():
            imgsList = imgsList.where(Images.owner == current_user)
            albumsList = albumsList.where(Albums.owner == current_user)
   
        pageString = self.getPageStr(
                            self.makeUrl('/admin/images/list'), 
                            page, 
                            config.COUNT_PER_PAGE, 
                            imgsList.count()
                     )
        self.privData['IMAGES_LIST'] = imgsList.order_by(Images.id.desc()).paginate(page, config.COUNT_PER_PAGE)
        self.privData['PAGE_STRING'] = pageString
        self.privData['ALBUMS_LIST'] = albumsList

        return self.display('imagesList')

    def search(self):
        inputParams = self.getInput()
        keywords = inputParams['keywords'].strip().lower() if inputParams.has_key('keywords') else ''
        page = int(inputParams['page']) if inputParams.has_key('page') else 1

        imgsList = Images.select().where(Images.description.contains(keywords))
        albumsList = Albums().select()
        current_user = Users.get(Users.name == self.isLogin())
        if not self.isAdmin():
            imgsList = imgsList.where(Images.owner == current_user)
            albumsList = albumsList.where(Albums.owner == current_user)
      
        pageString = self.getPageStr(
                        self.makeUrl('/admin/images/list'), 
                        page, 
                        config.COUNT_PER_PAGE, 
                        imgsList.count()
                     )
        self.privData['IMAGES_LIST'] = imgsList.order_by(Images.id.desc()).paginate(page, config.COUNT_PER_PAGE)
        self.privData['PAGE_STRING'] = pageString
        self.privData['ALBUMS_LIST'] = albumsList

        return self.display('imagesList')

    def search_by_album(self):
        inputParams = self.getInput()
        album = int(inputParams['album']) if inputParams.has_key('album') else 1
        page = int(inputParams['page']) if inputParams.has_key('page') else 1

        imgsList = Images.select().where(Images.album == album)
        albumsList = Albums().select()
        current_user = Users.get(Users.name == self.isLogin())
        if not self.isAdmin():
            imgsList = imgsList.where(Images.owner == current_user)
            albumsList = albumsList.where(Albums.owner == current_user)

   
        pageString = self.getPageStr(
                        self.makeUrl('/admin/images/list'), 
                        page, 
                        config.COUNT_PER_PAGE, 
                        imgsList.count()
                     )
        self.privData['IMAGES_LIST'] = imgsList.order_by(Images.id.desc()).paginate(page, config.COUNT_PER_PAGE)
        self.privData['PAGE_STRING'] = pageString
        self.privData['ALBUMS_LIST'] = albumsList

        return self.display('imagesList')

     
    def add(self):
        current_user = Users.get(Users.name == self.isLogin())
        albumsList = Albums().select()
        if not self.isAdmin():
            albumsList = albumsList.where(Albums.owner == current_user)

        if not albumsList.count():
            return self.error(msg = '请创建至少一个专辑!', url=self.makeUrl('/admin/albums/list'))

        self.privData['CURRENT_USER'] = current_user
        self.privData['ALBUMS_LIST'] = albumsList

        return self.display('imageAdd')


    def delete(self):
        inputParams = self.getInput()
        id = int(inputParams['id'])

        if id == 1:
            return self.error(msg = '不能删除系统图片!', url=self.makeUrl('/admin/images/list'))
        img = Images().get(Images.id == id)

        current_user = Users.get(Users.name == self.isLogin())
        if current_user.id != img.owner.id and not self.isAdmin():
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/images/list'))

        try:
            img.delete_instance()
            from uploadmgr import httpFileSystem as fs 
            os.unlink(fs().imageURIFromUUID(img.uuid))
        except Exception, e:
            return self.error(msg='对象删除失败: %s' % e, url=self.makeUrl('/admin/images/list'))
        
        return self.success(msg='对象删除成功', url=self.makeUrl('/admin/images/list'))


    def save(self):
        inputParams = self.getInput()

        id = int(inputParams['id'])
        if id == 1:
            return self.error(msg = '不能系统图片!', url=self.makeUrl('/admin/images/list'))
        img = Images().get(Images.id == id)

        current_user = Users.get(Users.name == self.isLogin())
        if current_user.id != img.owner.id and not self.isAdmin():
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/images/list'))
        
        try:
            img.description = self.htmlunquote(inputParams['desc'])
            img.album = int(inputParams['album'])
            img.save()
        except Exception, e:
            return self.error(msg='对象更新失败: %s' % e, url=self.makeUrl('/admin/images/list'))

        return self.success(msg='对象更新成功', url=self.makeUrl('/admin/images/list'))

    def edit(self):
        inputParams = self.getInput()

        id = int(inputParams['id'])
        img = Images().get(Images.id == id)

        current_user = Users.get(Users.name == self.isLogin())
        if current_user.id != img.owner.id and not self.isAdmin():
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/images/list'))

        albumsList = Albums().select()
        if not self.isAdmin():
            albumsList = albumsList.where(Albums.owner == current_user)

        if not albumsList.count():
            return self.error(msg = '请创建至少一个专辑!', url=self.makeUrl('/admin/albums/list'))

        self.privData['IMAGE_INFO'] = img
        self.privData['ALBUMS_LIST'] = albumsList

        return self.display('imageEdit')

    def thumbnail(self):
        inputParams = self.getInput()
        try:
            imageId = int(inputParams['id'])
            img = Images().get(Images.id == imageId)

            import base64
            return base64.b64decode(img.thumbnail)
        except Exception, e:
            from imaging import imaging
            return imaging.default_thumbnail()

    def getImages(self):
        result = {'status': 0, 'data': [], 'msg': 'success'}
        userInput= self.getInput()
        album = userInput.get('album', -1)
        if album == -1:
            result['status'] = -1
            result['msg'] = '未指定专辑'
            return json.dumps(result)
        imagesList = Images().select().where(Images.album == album)
        for img in imagesList:
            result['data'].append({
                'id': img.id,
                'desc': img.description,
                'url': self.makeUrl('/admin/images/thumbnail',{'id': img.id}),
                'src': self.imageUrl(img.id),
                })
        return json.dumps(result)
