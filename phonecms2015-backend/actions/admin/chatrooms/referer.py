# -*- coding: utf-8 -*-
#coding=utf-8

import config
from actions.admin.base import adminAction
from models.chatrooms import Chatrooms
from models.images import Images
from models.albums import Albums
from models.users import Users

'''
Admin controller: chatrooms administration views.
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
        
        current_user = Users.get(Users.name == self.isLogin())
        chatroomsList = Chatrooms.select().where(Chatrooms.owner==current_user)

        pageString = self.getPageStr(self.makeUrl('/admin/chatrooms/list'), page, count, chatroomsList.count())
        chatroomsList = chatroomsList.order_by(Chatrooms.id.desc())
        self.privData['CHATROOMS_LIST'] = chatroomsList.paginate(page, page+count)
        self.privData['PAGE_STRING'] = pageString
        self.privData['CHATROOMS_LIST'] = chatroomsList

        return self.display('chatroomsList')

    def delete(self):
        inputParams = self.getInput()

        try:
            chatroom = Chatrooms.get(Chatrooms.id == int(inputParams['id']))
            current_user = Users.get(Users.name == self.isLogin())
            if current_user.id != chatroom.owner.id and not self.isAdmin() or not current_user.role.type < 100:
                return self.error(msg = '权限不足!', url=self.makeUrl('/admin/chatrooms/list'))

            import leancloud
            leancloud.Apis().remove_conversation(chatroom.uuid)
            chatroom.delete_instance()
        except Exception, e:
            return self.error(msg = '删除聊天室失败: %s' % e, url=self.makeUrl('/admin/chatrooms/list'))
    
        return self.success(msg='删除聊天室成功', url=self.makeUrl('/admin/chatrooms/list'))

     
    def search(self):
        inputParams = self.getInput()
        keywords = inputParams['keywords'].strip().lower() if inputParams.has_key('keywords') else ''
        
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE

        current_user = Users.get(Users.name == self.isLogin())
        chatroomsList = Chatrooms.select().where(Chatrooms.name.contains(keywords)).where(Chatrooms.owner==current_user)
        pageString = self.getPageStr(self.makeUrl('/admin/chatrooms/list'), page, count, chatroomsList.count())
        chatroomsList = chatroomsList.order_by(Chatrooms.id.desc())
        self.privData['CHATROOMS_LIST'] = chatroomsList.paginate(page, page+count)
        self.privData['PAGE_STRING'] = pageString
        self.privData['CHATROOMS_LIST'] = chatroomsList
        return self.display('chatroomsList')

        
    def add(self):
        chatroomsList = Chatrooms().select()

        userName = self.isLogin()
        if userName != 'admin':
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/chatrooms/list'))
        user = Users.get(Users.name == userName)
        albumsList = Albums().select().where(Albums.owner == user.id)
        imagesList = Images().select().where(Images.owner == user.id)

        if not albumsList.count():
            return self.error(msg = '请创建至少一个专辑!', url=self.makeUrl('/admin/chatrooms/list'))
        if not imagesList.count():
            return self.error(msg = '请创建至少一个图片!', url=self.makeUrl('/admin/chatrooms/list'))

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

        # 默认专辑为当前用户的第一个专辑
        self.privData['CURRENT_ALBUM'] = self.privData['ALBUMS_LIST'][0]
        # 默认图片为默认专辑的第一张图片
        self.privData['CURRENT_IMG'] = album_images_map[self.privData['CURRENT_ALBUM'].id][0]
        self.privData['SUBMIT_NAME'] = "thumbnail"

        return self.display('chatroomAdd')

    def modify(self):
        inputParams= self.getInput()
         
        try:
            chatroomId = int(inputParams['id'])
            chatroom = Chatrooms.get(Chatrooms.id == chatroomId)

            current_user = Users.get(Users.name == self.isLogin())
            if current_user.id != chatroom.owner.id and not self.isAdmin() or not current_user.role.type < 100:
                return self.error(msg = '权限不足!', url=self.makeUrl('/admin/chatrooms/list'))

            q = Chatrooms.update(
                name = inputParams['name'],
                description = inputParams['desc'],
                thumbnail = int(inputParams['thumbnail']),
            ).where(Chatrooms.id == chatroomId)
            q.execute()
        except Exception, e:
            return self.error(msg = '聊天室修改失败: %s' % e, url=self.makeUrl('/admin/chatrooms/list'))

        return self.success('聊天室修改成功', url=self.makeUrl('/admin/chatrooms/list'))

    def edit(self):
        inputParams = self.getInput()
        userName = self.isLogin()

        chatroomID = int(inputParams['id'])
        # 权限检查
        chatroom = Chatrooms.get(Chatrooms.id == chatroomID)
        current_user = Users.get(Users.name == self.isLogin())
        if current_user.id != chatroom.owner.id and not self.isAdmin() or not current_user.role.type < 100:
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/chatrooms/list'))

        self.privData['CHATROOM'] = chatroom

        user = Users.get(Users.name == userName)
        albumsList = Albums().select().where(Albums.owner == user.id)
        imagesList = Images().select().where(Images.owner == user.id)

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

        self.privData['CURRENT_CHATROOM'] = chatroom
        self.privData['CURRENT_ALBUM'] = chatroom.thumbnail.album
        self.privData['CURRENT_IMG'] = chatroom.thumbnail
        self.privData['SUBMIT_NAME'] = "thumbnail"

        return self.display('chatroomEdit')


    def save(self):
        userInput = self.getInput()  
        try:
            current_user = Users.get(Users.name == self.isLogin())
            thumbnail = int(userInput['thumbnail']);

            import leancloud
            conversation = leancloud.Apis().create_conversation(userInput['name'], current_user.name)

            Chatrooms.create(
                name = userInput['name'],
                owner = current_user,
                thumbnail = thumbnail,
                uuid = conversation,
                description = userInput['desc']
            )
          
        except Exception, e:
            return self.error(msg = '新增聊天室失败: %s' % e, url=self.makeUrl('/admin/chatrooms/list'))

        return self.success('新增聊天室成功', url=self.makeUrl('/admin/chatrooms/list'))
