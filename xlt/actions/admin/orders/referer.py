# -*- coding: utf-8 -*-
#coding=utf-8

import config
from actions.admin.base import adminAction
from models.orders import Orders
from models.users import Users
from models.products import Products
from models.images import Images

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
        else:
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
        count = config.COUNT_PER_PAGE

        ordersList = Orders.select().order_by(Orders.id.desc())
        pageString = self.getPageStr(self.makeUrl('/admin/orders/list'), page, count, ordersList.count())
        self.privData['ORDERS_LIST'] = ordersList.paginate(page, count)
        self.privData['PAGE_STRING'] = pageString
        return self.display('ordersList')

    def delete(self):
        inputParams = self.getInput()

        try:
            order = Orders.get(Orders.id == int(inputParams['id']))
            order.delete_instance()
        except Exception, e:
            return self.error(msg = '删除失败: %s' % e, url=self.makeUrl('/admin/orders/list'))
    
        return self.success(msg='删除成功', url=self.makeUrl('/admin/orders/list'))

     
    def search(self):
        inputParams = self.getInput()
        keywords = inputParams['keywords'].strip().lower() if inputParams.has_key('keywords') else ''
        
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE

        ordersList = Orders.select().where(Orders.name.contains(keywords)).order_by(Orders.id.desc())
        pageString = self.getPageStr(self.makeUrl('/admin/orders/list'), page, count, ordersList.count())
        self.privData['NEWS_LIST'] = ordersList.paginate(page, count)
        self.privData['PAGE_STRING'] = pageString
        return self.display('ordersList')
