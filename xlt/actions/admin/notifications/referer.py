# -*- coding: utf-8 -*-
#coding=utf-8

import config
from actions.admin.base import adminAction
from models.notifications import Notifications
from models.images import Images
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

        notificationsList = Notifications.select()

        pageString = self.getPageStr(self.makeUrl('/admin/notifications/list'), page, count, notificationsList.count())
        notificationsList = notificationsList.order_by(Notifications.id.desc())
        self.privData['NOTIFICATIONS_LIST'] = notificationsList.paginate(page, count)
        self.privData['PAGE_STRING'] = pageString

        return self.display('notificationsList')

    def delete(self):
        inputParams = self.getInput()

        try:
            notification = Notifications.get(Notifications.id == int(inputParams['id']))
            notification.delete_instance()
        except Exception, e:
            return self.error(msg = '删除失败: %s' % e, url=self.makeUrl('/admin/notifications/list'))
    
        return self.success(msg='删除成功', url=self.makeUrl('/admin/notifications/list'))

     
    def search(self):
        inputParams = self.getInput()
        keywords = inputParams['keywords'].strip().lower() if inputParams.has_key('keywords') else ''
        
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE

        notificationsList = Notifications.select().where(Notifications.name.contains(keywords))
        pageString = self.getPageStr(self.makeUrl('/admin/notifications/list'), page, count, notificationsList.count())
        notificationsList = notificationsList.order_by(Notifictions.id.desc())
        self.privData['NOTIFICATIONS_LIST'] = notificationsList.paginate(page, count)
        self.privData['PAGE_STRING'] = pageString
        return self.display('notificationsList')

        
    def add(self):
        imagesList = Images().select()

        if not imagesList.count():
            return self.error(msg = '请创建至少一个图片!', url=self.makeUrl('/admin/images/list'))

        self.privData['IMAGES_LIST'] = imagesList
        self.privData['CURRENT_IMG'] = imagesList[0]
        self.privData['SUBMIT_NAME'] = "thumbnail"

        return self.display('notificationAdd')

    def modify(self):
        inputParams= self.getInput()
         
        try:
            notification_id = int(inputParams['id'])
            notification = Notifications().get(Notifications.id == notification_id)
            notification.name = inputParams['name']
            notification.content = inputParams['content']
            notification.thumbnail = inputParams['thumbnail']
            notification.emoji = inputParams['emoji']
            notification.save()
        except Exception, e:
            return self.error(msg = '信息修改失败: %s' % e, url=self.makeUrl('/admin/notifications/list'))

        return self.success('信息修改成功', url=self.makeUrl('/admin/notifications/list'))

    def edit(self):
        inputParams = self.getInput()
        notificationID = int(inputParams['id'])
        notification = Notifications.get(Notifications.id == notificationID)
        self.privData['NOTIFICATION'] =   notification

        imagesList = Images().select()
        if not imagesList.count():
            return self.error(msg = '请创建至少一个图片!', url=self.makeUrl('/admin/images/list'))


        self.privData['IMAGES_LIST'] = imagesList
        self.privData['CURRENT_IMG'] = notification.thumbnail
        self.privData['SUBMIT_NAME'] = "thumbnail"

        return self.display('notificationEdit')


    def save(self):
        userInput = self.getInput()  
        try:
            thumbnail = int(userInput['thumbnail']);
            Notifications.create(
                name = userInput['name'],
                thumbnail = thumbnail,
                emoji = userInput['emoji'],
                content = userInput['content']
            )          
        except Exception, e:
            return self.error(msg = '新增失败: %s' % e, url=self.makeUrl('/admin/notifications/list'))

        return self.success('新增成功', url=self.makeUrl('/admin/notifications/list'))
