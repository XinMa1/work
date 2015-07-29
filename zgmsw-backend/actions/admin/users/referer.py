# -*- coding: utf-8 -*-
#coding=utf-8

import web
import os
import config
import hashlib
from actions.admin.base import adminAction
from models.users import Users
from models.albums import Albums
from models.images import Images
from models.roles import Roles

'''
Admin controller: producing user administration views.
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
        elif name == 'pwdedit':
            return self.pwdedit()            

        return self.notFound()

    def POST(self, name):
        if name == 'save':
            return self.save()
        elif name == 'modify':
            return self.modify()
        elif name == 'savepwd':
            return self.savepwd()


        return self.notFound()

    def list(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE
        offset= (page-1)*count if page > 0 else 0

        current_user = Users.get(Users.name == self.isLogin())   
        usersList = Users().select()
        if not self.isAdmin():
            usersList = usersList.where(Users.id == current_user)

        usersList = usersList.order_by(Users.id.desc())
        pageString = self.getPageStr('/admin/users/list', page, count, usersList.count())
        self.privData['USERS_LIST'] = usersList
        self.privData['PAGE_STRING'] = pageString
        return self.display('usersList')


    def delete(self):
        inputParams = self.getInput()
        user_id = int(inputParams['id'])

        # 只有admin才能删除用户
        if not self.isAdmin():
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/users/list'))

        if user_id == 1:
            return self.error(msg='不能删除admin', url=self.makeUrl('/admin/users/list'))

        try:
            user = Users.get(Users.id == user_id)
            user.delete_instance()
        except Exception, e:
            return self.success(msg='会员删除失败: %s' % e, url=self.makeUrl('/admin/users/list'))

        return self.success(msg='会员删除成功', url=self.makeUrl('/admin/users/list'))

    def add(self):
        if not self.isAdmin():
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/users/list'))


        albumsList = Albums().select()
        imagesList = Images().select()

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

        # 不允许创建系统管理员
        rolesList = Roles().select().where(Roles.id>1)
        self.privData['ROLES_LIST'] = rolesList

        self.privData['ALBUMS_LIST'] = \
            [album for album in albumsList if album.id not in excluded_albums]
        self.privData['IMG_ALBUMS_LIST'] = album_images_map
        self.privData['CURRENT_ALBUM'] = self.privData['ALBUMS_LIST'][0]
        self.privData['CURRENT_IMG'] = album_images_map[self.privData['CURRENT_ALBUM'].id][0]
        self.privData['SUBMIT_NAME'] = "thumbnail"

        return self.display('userAdd')
    
    def modify(self):
        userInput= self.getInput()

        userObj = Users.get(Users.id == int(userInput['id']))
        current_user = Users.get(Users.name == self.isLogin())   

        if userObj.id != current_user.id and not self.isAdmin():
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/users/list'))

        thumbnail_id = int(userInput['thumbnail']) if userInput.has_key('thumbnail') else 0
        if thumbnail_id:
            thumbnail_data = Images.get(Images.id == thumbnail_id).thumbnail
        else:
            import base64
            from imaging import imaging
            thumbnail_data = base64.b64encode(buffer(imaging.default_thumbnail()))

        try:
            userObj = Users.get(Users.id == int(userInput['id']))
            userObj.email = userInput['email']
            userObj.name = userInput['name']
            userObj.cellphone = userInput['cellphone']
            userObj.description = userInput['desc']
            userObj.gender = int(userInput['gender'])
            userObj.avatur = thumbnail_data
            if self.isAdmin():
                userObj.role = userInput['role']
            userObj.save()
        except Exception, e:
            return self.error(msg = '会员修改失败: %s' % e, url=self.makeUrl('/admin/users/list'))

        return self.success('会员修改成功', url=self.makeUrl('/admin/users/list'))

    def edit(self):
        inputParams = self.getInput()

        userObj = Users.get(Users.id == int(inputParams['id']))
        current_user = Users.get(Users.name == self.isLogin())   

        if userObj.id != current_user.id and not self.isAdmin():
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/users/list'))

        # 不允许创建系统管理员
        rolesList = Roles().select().where(Roles.id>1)
        self.privData['ROLES_LIST'] = rolesList

        self.privData['USER_INFO'] = userObj

        albumsList = Albums().select()
        imagesList = Images().select()

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
        self.privData['IMG_ALBUMS_LIST'] = album_images_map
        self.privData['CURRENT_ALBUM'] = self.privData['ALBUMS_LIST'][0]
        self.privData['CURRENT_IMG'] = album_images_map[self.privData['CURRENT_ALBUM'].id][0]
        self.privData['SUBMIT_NAME'] = "thumbnail"

        return self.display('userEdit')

    def pwdedit(self):
        inputParams = self.getInput()

        userID = inputParams['id']
        userObj = Users().get(Users.id == userID)
        if not userObj:
            return self.error(msg = '该会员不存在', url=self.makeUrl('/admin/users/list'))

        self.privData['USER_INFO'] = userObj

        return self.display('changePwd')

    def savepwd(self):
        inputData = self.getInput()
        #password = hashlib.md5(inputData['oldpwd']).hexdigest() 
        userID = inputData['id']
        newpwd1 = hashlib.md5(inputData['newpwdone']).hexdigest()
        newpwd2 = hashlib.md5(inputData['newpwdtwo']).hexdigest()

        
        if newpwd1 != newpwd2:
            return self.error(msg = '两次密码输入不一致', url=self.makeUrl('/admin/users/list'))
     
        user = Users.get(Users.id == userID)
        user.password = newpwd1

        try:
            user = Users.get(Users.id == userID)
            user.password = newpwd1
        except Exception, e:
            return self.error(msg = '会员密码修改失败: %s' % e, url=self.makeUrl('/admin/users/list'))

        return self.success('会员密码修改成功', url=self.makeUrl('/admin/users/list'))

    def save(self):
        userInput = self.getInput()  
        # 只有admin才能新增用户
        if not self.isAdmin():
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/users/list'))

        thumbnail_id = int(userInput['thumbnail']) if userInput.has_key('thumbnail') else 0
        if thumbnail_id:
            thumbnail_data = Images.get(Images.id == thumbnail_id).thumbnail
        else:
            import base64
            from imaging import imaging
            thumbnail_data = base64.b64encode(buffer(imaging.default_thumbnail()))

        try:
            Users.create(
                cellphone = userInput['cellphone'],
                email = userInput['email'],
                name = userInput['name'],
                password = hashlib.md5(userInput['passwd']).hexdigest(),
                avatur = thumbnail_data,
                gender = int(userInput['gender']),
                description = userInput['desc'],
                role = int(userInput['role'])
            )
        except Exception, e:
            return self.error(msg = '会员保存失败: %s' % e, url=self.makeUrl('/admin/users/list'))

        return self.success('会员保存成功', url=self.makeUrl('/admin/users/list'))
