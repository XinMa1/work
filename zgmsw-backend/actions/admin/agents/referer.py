# -*- coding: utf-8 -*-
#coding=utf-8

import config
from actions.admin.base import adminAction
from models.agents import Agents
from models.images import Images
from models.albums import Albums
from models.users import Users

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

        agentsList = Agents.select()

        pageString = self.getPageStr(self.makeUrl('/admin/agents/list'), page, count, agentsList.count())
        agentsList = agentsList.order_by(Agents.id.desc())
        self.privData['AGENTS_LIST'] = agentsList.paginate(page, page+count)
        self.privData['PAGE_STRING'] = pageString
        self.privData['AGENTS_LIST'] = agentsList

        return self.display('agentsList')

    def delete(self):
        inputParams = self.getInput()

        try:
            current_user = Users.get(Users.name == self.isLogin())
            if  not self.isAdmin():
                return self.error(msg = '权限不足!', url=self.makeUrl('/admin/agents/list')) 
            agent = Agents.get(Agents.id == int(inputParams['id']))
            agent.delete_instance()
        except Exception, e:
            return self.error(msg = '删除代理机构失败: %s' % e, url=self.makeUrl('/admin/agents/list'))
    
        return self.success(msg='删除代理机构成功', url=self.makeUrl('/admin/agents/list'))

     
    def search(self):
        inputParams = self.getInput()
        keywords = inputParams['keywords'].strip().lower() if inputParams.has_key('keywords') else ''
        
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE

        agentsList = Agents.select().where(Agents.name.contains(keywords))
        pageString = self.getPageStr(self.makeUrl('/admin/agents/list'), page, count, agentsList.count())
        agentsList = agentsList.order_by(Agents.id.desc())
        self.privData['AGENTS_LIST'] = agentsList.paginate(page, page+count)
        self.privData['PAGE_STRING'] = pageString
        self.privData['AGENTS_LIST'] = agentsList
        return self.display('agentsList')

        
    def add(self):
        agentsList = Agents().select()

        userName = self.isLogin()
        if userName != 'admin':
            return self.error(msg = '只有admin用户可以使用创建培训机构功能',url=self.makeUrl('/admin/agents/list'))
        user = Users.get(Users.name == userName)
        albumsList = Albums().select().where(Albums.owner == user.id)
        imagesList = Images().select().where(Images.owner == user.id)

        if not albumsList.count():
            return self.error(msg = '请创建至少一个专辑!', url=self.makeUrl('/admin/agents/list'))
        if not imagesList.count():
            return self.error(msg = '请创建至少一个图片!', url=self.makeUrl('/admin/agents/list'))

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

        return self.display('agentAdd')

    def modify(self):
        inputParams= self.getInput()
         
        try:
            agent_id = int(inputParams['id'])
            agent = Agents().get(Agents.id == agent_id)
            agent.name = inputParams['name']
            agent.content = inputParams['content']
            agent.thumbnail = inputParams['thumbnail']
            agent.save()
        except Exception, e:
            return self.error(msg = '信息修改失败: %s' % e, url=self.makeUrl('/admin/agents/list'))

        return self.success('信息修改成功', url=self.makeUrl('/admin/agents/list'))

    def edit(self):
        inputParams = self.getInput()
        userName = self.isLogin()
        if userName != 'admin':
            return self.error(msg = '只有admin可以编辑',url=self.makeUrl('/admin/agents/list'))

        agentID = int(inputParams['id'])
        agent = Agents.get(Agents.id == agentID)

        self.privData['AGENT'] =   agent

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

        self.privData['CURRENT_AGENT'] = agent
        self.privData['CURRENT_ALBUM'] = agent.thumbnail.album
        self.privData['CURRENT_IMG'] = agent.thumbnail
        self.privData['SUBMIT_NAME'] = "thumbnail"

        return self.display('agentEdit')


    def save(self):
        userInput = self.getInput()  
        try:
            if not self.isAdmin():
                return self.error(msg = '权限不足!', url=self.makeUrl('/admin/agents/list'))

            thumbnail = int(userInput['thumbnail']);
            Agents.create(
                name = userInput['name'],
                thumbnail = thumbnail,
                content = userInput['content']
            )
          
        except Exception, e:
            return self.error(msg = '新增代理失败: %s' % e, url=self.makeUrl('/admin/agents/list'))

        return self.success('新增代理成功', url=self.makeUrl('/admin/agents/list'))
