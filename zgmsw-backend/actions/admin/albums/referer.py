# -*- coding: utf-8 -*-
#coding=utf-8

import config
from actions.admin.base import adminAction
from models.albums import Albums
from models.users import Users
from models.images import Images

'''
Admin controller: producing album administration views.
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
         
        albumsList = Albums().select()
        current_user = Users.get(Users.name == self.isLogin())
        if not self.isAdmin():
            albumsList = albumsList.where(Albums.owner == current_user)

        albumsList = albumsList.order_by(Albums.id.desc())
        pageString = self.getPageStr(
                        self.makeUrl('/admin/albums/list'), 
                        page, 
                        config.COUNT_PER_PAGE, 
                        albumsList.count()
                     )

        self.privData['ALBUMS_LIST'] = albumsList.paginate(page, config.COUNT_PER_PAGE)
        self.privData['PAGE_STRING'] = pageString

        return self.display('albumsList')

    def delete(self):
        inputParams = self.getInput()
        album_id = int(inputParams['id'])

        if album_id == 1:
            return self.error(msg='不能删除系统专辑', url=self.makeUrl('/admin/albums/list'))

        album = Albums.get(Albums.id == album_id)
        current_user = Users.get(Users.name == self.isLogin())
        if current_user.id != album.owner.id and not self.isAdmin():
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/albums/list'))

        try:
            album.delete_instance()
        except Exception, e:
            return self.error(msg = '专辑删除失败: %s' % e, url=self.makeUrl('/admin/albums/list'))
    
        return self.success(msg='专辑删除成功', url=self.makeUrl('/admin/albums/list'))

     
    def search(self):
        inputParams = self.getInput()
        keywords = inputParams['keywords'].strip().lower() if inputParams.has_key('keywords') else ''
        page = int(inputParams['page']) if inputParams.has_key('page') else 1

        albumsList = Albums().select().where(Albums.name.contains(keywords))
        current_user = Users.get(Users.name == self.isLogin())
        if not self.isAdmin():
            albumsList = albumsList.where(Albums.owner == current_user)

        pageString = self.getPageStr(
                        self.makeUrl('/admin/albums/list'), 
                        page, 
                        config.COUNT_PER_PAGE, 
                        albumsList.count()
                     )
        self.privData['ALBUMS_LIST'] = albumsList.paginate(page, config.COUNT_PER_PAGE)
        self.privData['PAGE_STRING'] = pageString

        return self.display('albumsList')

        
    def add(self):
        return self.display('albumAdd')

    def modify(self):
        inputParams= self.getInput()
        album_id = int(inputParams['id'])
        thumbnail_id = int(inputParams['thumbnail']) if inputParams.has_key('thumbnail') else 0
 
        if album_id == 1:
            return self.error(msg='不能编辑系统专辑', url=self.makeUrl('/admin/albums/list'))

        album = Albums.get(Albums.id == album_id)
        current_user = Users.get(Users.name == self.isLogin())
        if current_user.id != album.owner.id and not self.isAdmin():
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/albums/list'))

        if thumbnail_id:
            thumbnail_data = Images.get(Images.id == thumbnail_id).thumbnail
        else:
            import base64
            from imaging import imaging
            thumbnail_data = base64.b64encode(buffer(imaging.default_thumbnail()))

        try:
            album.name  = inputParams['name']
            album.description = inputParams['desc']
            album.thumbnail = thumbnail_data
            album.save()
        except Exception, e:
            return self.error(msg = '专辑修改失败: %s' % e, url=self.makeUrl('/admin/albums/list'))

        return self.success('专辑修改成功', url=self.makeUrl('/admin/albums/list'))

    def edit(self):
        inputParams = self.getInput()
        album_id = int(inputParams['id'])
        album = Albums.get(Albums.id == album_id)

        current_user = Users.get(Users.name == self.isLogin())
        if current_user.id != album.owner.id and not self.isAdmin():
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/albums/list'))

        self.privData['ALBUM_ID'] =   album.id
        self.privData['ALBUM_NAME'] = album.name
        self.privData['ALBUM_DESC'] = album.description
        self.privData['ENABLE_SELECT_THUMBNAIL'] = False

        imagesList = Images().select()
        if not self.isAdmin():
            imagesList = imagesList.where(Images.owner == current_user)

        imagesList = imagesList.where(Images.album == album)
        if imagesList.count():
            self.privData['ENABLE_SELECT_THUMBNAIL'] = True
            self.privData['ALBUMS_LIST'] = [album]
            self.privData['IMG_ALBUMS_LIST'] = {album.id: imagesList}
            self.privData['CURRENT_IMG'] = imagesList[0]
            self.privData['CURRENT_ALBUM'] = album
            self.privData['SUBMIT_NAME'] = "thumbnail"

        return self.display('albumEdit')


    def save(self):
        userInput = self.getInput() 

        try:
            import base64
            from imaging import imaging
            thumbnail_data = base64.b64encode(buffer(imaging.default_thumbnail()))
                
            Albums.create(
                name = userInput['name'],
                description = userInput['desc'],
                thumbnail = thumbnail_data,
                owner = Users.get(Users.name == self.isLogin())
            )
        except Exception, e:
            return self.error(msg = '专辑保存失败: %s' % e, url=self.makeUrl('/admin/albums/list'))

        return self.success('专辑保存成功', url=self.makeUrl('/admin/albums/list'))
