# -*- coding: utf-8 -*-
#coding=utf-8

import web
import os
import config
import hashlib
from actions.admin.base import adminAction
from models.contacts import Contacts
from models.images import Images

'''
Admin controller: producing contact administration views.
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

        return self.notFound()

    def POST(self, name):
        if name == 'save':
            return self.save()
        elif name == 'modify':
            return self.modify()

        return self.notFound()

    def list(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE

        contactsList = contactsList = Contacts().select().order_by(Contacts.id.desc())
        pageString = self.getPageStr('/admin/contacts/list', page, count, contactsList.count())
        self.privData['CONTACTS_LIST'] = contactsList.paginate(page, count)
        self.privData['PAGE_STRING'] = pageString
        return self.display('contactsList')


    def delete(self):
        inputParams = self.getInput()
        contact_id = int(inputParams['id'])

        try:
            contact = Contacts.get(Contacts.id == contact_id)
            contact.delete_instance()
        except Exception, e:
            return self.success(msg='删除失败: %s' % e, url=self.makeUrl('/admin/contacts/list'))

        return self.success(msg='删除成功', url=self.makeUrl('/admin/contacts/list'))

    def add(self):
        imagesList = Images().select()

        if not imagesList.count():
            return self.error(msg = '请创建至少一个图片!', url=self.makeUrl('/admin/images/list'))

        self.privData['IMAGES_LIST'] = imagesList
        self.privData['CURRENT_IMG'] = imagesList[0]
        self.privData['SUBMIT_NAME'] = "thumbnail"

        return self.display('contactAdd')
    
    def modify(self):
        inputParams= self.getInput()

        try:
            contactObj = Contacts.get(Contacts.id == int(inputParams['id']))
            contactObj.email = inputParams['email']
            contactObj.name = inputParams['name']
            contactObj.sn = inputParams['sn']
            contactObj.weixin = inputParams['weixin']
            contactObj.title = inputParams['title']
            contactObj.address = inputParams['address']
            contactObj.cellphone = inputParams['cellphone']
            contactObj.description = inputParams['desc']
            contactObj.gender = int(inputParams['gender'])
            contactObj.avatur = int(inputParams['thumbnail'])
            contactObj.save()
        except Exception, e:
            return self.error(msg = '修改失败: %s' % e, url=self.makeUrl('/admin/contacts/list'))

        return self.success('修改成功', url=self.makeUrl('/admin/contacts/list'))

    def edit(self):
        inputParams = self.getInput()

        imagesList = Images().select()
        if not imagesList.count():
            return self.error(msg = '请创建至少一个图片!', url=self.makeUrl('/admin/images/list'))
        try:
            contactObj = Contacts.get(Contacts.id == int(inputParams['id']))
        except Exception, e:
            return self.error(msg = '对象不存在: %s' % e, url=self.makeUrl('/admin/contacts/list'))

        self.privData['IMAGES_LIST'] = imagesList
        self.privData['CONTACT_INFO'] = contactObj
        self.privData['CURRENT_IMG'] = contactObj.avatur
        self.privData['SUBMIT_NAME'] = "thumbnail"

        return self.display('contactEdit')


    def save(self):
        inputParams = self.getInput()  

        try:
            Contacts.create(
                cellphone = inputParams['cellphone'],
                email = inputParams['email'],
                name = inputParams['name'],
                sn = inputParams['sn'],
                weixin = inputParams['weixin'],
                title = inputParams['title'],
                address = inputParams['address'],
                avatur = int(inputParams['thumbnail']),
                gender = int(inputParams['gender']),
                description = inputParams['desc'],
            )
        except Exception, e:
            return self.error(msg = '保存失败: %s' % e, url=self.makeUrl('/admin/contacts/list'))

        return self.success('保存成功', url=self.makeUrl('/admin/contacts/list'))
