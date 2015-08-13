# -*- coding: utf-8 -*-
#coding=utf-8

import web
import os
import json
import config
from actions.admin.base import adminAction
from models.images import Images

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

        return self.notFound()

    def POST(self, name):
        if name == 'save':
            return self.save()
        elif name == 'search':
            return self.search()
        else:
            return self.notFound()

    def list(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1

        imgsList = Images.select().order_by(Images.id.desc())   
        pageString = self.getPageStr(
                            self.makeUrl('/admin/images/list'), 
                            page, 
                            config.COUNT_PER_PAGE, 
                            imgsList.count()
                     )
        self.privData['IMAGES_LIST'] = imgsList.paginate(page, config.COUNT_PER_PAGE)
        self.privData['PAGE_STRING'] = pageString
        return self.display('imagesList')

    def search(self):
        inputParams = self.getInput()
        keywords = inputParams['keywords'].strip().lower() if inputParams.has_key('keywords') else ''
        page = int(inputParams['page']) if inputParams.has_key('page') else 1

        imgsList = Images.select().where(Images.description.contains(keywords)).order_by(Images.id.desc())
        pageString = self.getPageStr(
                        self.makeUrl('/admin/images/list'), 
                        page, 
                        config.COUNT_PER_PAGE, 
                        imgsList.count()
                     )
        self.privData['IMAGES_LIST'] = imgsList.paginate(page, config.COUNT_PER_PAGE)
        self.privData['PAGE_STRING'] = pageString

        return self.display('imagesList')

     
    def add(self):
        return self.display('imageAdd')


    def delete(self):
        inputParams = self.getInput()
        id = int(inputParams['id'])

        if id == 1:
            return self.error(msg = '不能删除系统图片!', url=self.makeUrl('/admin/images/list'))

        try:
            img = Images().get(Images.id == id)
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
        try:
            img = Images().get(Images.id == id)
            img.description = self.htmlunquote(inputParams['desc'])
            img.save()
        except Exception, e:
            return self.error(msg='对象更新失败: %s' % e, url=self.makeUrl('/admin/images/list'))

        return self.success(msg='对象更新成功', url=self.makeUrl('/admin/images/list'))

    def edit(self):
        inputParams = self.getInput()

        id = int(inputParams['id'])
        img = Images().get(Images.id == id)
        self.privData['IMAGE_INFO'] = img

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
        imagesList = Images().select()
        for img in imagesList:
            result['data'].append({
                'id': img.id,
                'desc': img.description,
                'url': self.makeUrl('/admin/images/thumbnail',{'id': img.id}),
                'src': self.imageUrl(img.id),
                })
        return json.dumps(result)

