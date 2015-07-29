# -*- coding: utf-8 -*-
#coding=utf-8

import config
import os
from actions.admin.base import adminAction
from models.alipayconfig import Alipayconfig

'''
Admin controller: producing alipayconfig administration views.
'''
class refererAction(adminAction):
    def __init__(self):
        adminAction.__init__(self)

    def GET(self, name):
        if name == 'edit':
            return self.edit()
        elif name == 'new':
            return self.new()
        elif name == 'show':
            return self.show()
        return self.notFound()

    def POST(self, name):
        if name == 'save':
            return self.save()
        elif name == 'update':
            return self.update()
        return self.notFound()

    def edit(self):
        inputParams= self.getInput()
        alipayconfigObj = Alipayconfig.get()
        if not alipayconfigObj:
            return self.error(msg = '指定id的支付配置不存在', url=self.makeUrl('/admin/alipay/show'))
        self.privData['ALIPAY'] = alipayconfigObj

        return self.display('alipayconfigEdit')

    def new(self):
        alipayconfigObj = Alipayconfig.get()
        if alipayconfigObj:
            return self.error(msg = '已经存在支付配置,不能新建', url=self.makeUrl('/admin/alipay/show'))
        return self.display('alipayconfigNew')

    def save(self):
        alipayconfigObj = Alipayconfig.get()
        if alipayconfigObj:
            return self.error(msg = '保存失败: 已经存在支付配置,不能新建', url=self.makeUrl('/admin/alipay/show'))

        inputParams= self.getInput()
        try:
            Alipayconfig.create(
                partner = inputParams['partner'],
                key = inputParams['key'],
                seller_email = inputParams['seller_email']
            )
        except Exception, e:
            return self.error(msg = '新增失败: %s' % e, url=self.makeUrl('/admin/alipay/show'))

        return self.success('保存成功', url=self.makeUrl('/admin/alipay/show'))

    def show(self):
        alipayconfigObj = Alipayconfig.get()
        if not alipayconfigObj:
            alipayconfigObj={
                'id': -1,
                'partner': '[无记录,请新建]',
                'key': '[无记录,请新建]',
                'seller_email': '[无记录,请新建]',
            }
        self.privData['ALIPAY'] = alipayconfigObj
        return self.display('alipayconfigShow')

    def update(self):
        inputParams= self.getInput()
        alipayconfigObj = Alipayconfig.get(Alipayconfig.id == inputParams['id'])
        try:
            alipayconfigObj.partner = inputParams['partner']
            alipayconfigObj.key = inputParams['key']
            alipayconfigObj.seller_email = inputParams['seller_email']
            alipayconfigObj.save()
        except Exception, e:
            return self.error(msg = '保存失败: %s' % e, url=self.makeUrl('/admin/alipay/edit'))

        return self.success('保存成功', url=self.makeUrl('/admin/alipay/show'))
