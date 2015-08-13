# -*- coding: utf-8 -*-
#coding=utf-8

import config
from actions.admin.base import adminAction
from models.categories import Categories
from models.products import Products
'''
Admin controller: producing product administration views.
'''
class refererAction(adminAction):
    def __init__(self):
        adminAction.__init__(self)

    def GET(self, name):
        if name == 'list':
            return self.list()
        elif name == 'add':
            return self.add()
        elif name == 'delete':
            return self.delete()
        elif name == 'edit':
            return self.edit()

        return self.notFound()

    def POST(self, name):
        if name == 'save':
            return self.save()
        elif name == 'update':
            return self.update()
        elif name == 'search':
            return self.search()
        elif name == 'search_by_category':
	        return self.search_by_category()

        return self.notFound()

    def list(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE
   
        productsList = Products.select().order_by(Products.id.desc())
        pageString = self.getPageStr('/admin/products/list', page, count, productsList.count())
        self.privData['PRODUCTS_LIST'] = productsList.paginate(page, count)
        self.privData['PAGE_STRING'] = pageString

        categoriesList = Categories().select()
        self.privData['CATEGORIES_LIST'] = categoriesList
        return self.display('productsList')

    def search(self):
        inputParams = self.getInput()
        keywords = inputParams['keywords'].strip().lower() if inputParams.has_key('keywords') else ''

        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE

        productsList = Products.select().where(Products.name.contains(keywords)).order_by(Products.id.desc())

        pageString = self.getPageStr('/admin/products/list', page, count, productsList.count())
        self.privData['PRODUCTS_LIST'] = productsList.paginate(page, count)
        self.privData['PAGE_STRING'] = pageString

        categoriesList = Categories().select()
        self.privData['CATEGORIES_LIST'] = categoriesList

        return self.display('productsList')

    def search_by_category(self):
        inputParams = self.getInput()
        category = int(inputParams['category']) if inputParams.has_key('category') else 0
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE
        offset= (page-1)*count if page > 0 else 0

        productsList = Products.select().where(Products.category == category).order_by(Products.id.desc())
        pageString = self.getPageStr('/admin/products/list', page, count, productsList.count())
        self.privData['PRODUCTS_LIST'] = productsList
        self.privData['PAGE_STRING'] = pageString
        categoriesList = Categories().select()
        self.privData['CATEGORIES_LIST'] = categoriesList

        return self.display('productsList')

        
    def delete(self):
        inputParams = self.getInput()

        try:
            product = Products.get(Products.id == int(inputParams['id']))
            product.delete_instance()
        except Exception, e:
            return self.success(msg='删除失败: %s' % e, url=self.makeUrl('/admin/products/list'))

        return self.success(msg='删除成功', url=self.makeUrl('/admin/products/list'))

    def edit(self):
        inputParams = self.getInput()
        productID = inputParams['id']

        current_product = Products().get(Products.id == productID)

        categoriesList = Categories().select()
        self.privData['CATEGORIES_LIST'] = categoriesList
        self.privData['CURRENT_PRODUCT'] = current_product 

        return self.display('productEdit')

    def update(self):
        inputParams= self.getInput() 
        product = Products.get(Products.id == int(inputParams['id']))

        try:
            product.name = inputParams['name']
            product.description = self.htmlunquote(inputParams['desc'])
            product.category = int(inputParams['category'])
            product.diameter = inputParams['diameter']
            product.price1 = inputParams['price1']
            product.price2 = inputParams['price2']
            product.type = int(inputParams['type'])
            product.save()
        except Exception, e:
            return self.error(msg = '修改失败: %s' % e, url=self.makeUrl('/admin/products/list'))

        return self.success('修改成功!', url=self.makeUrl('/admin/products/list'))

    def add(self):
        categoriesList = Categories().select()

        self.privData['CATEGORIES_LIST'] = categoriesList
        return self.display('productAdd')


    def save(self):
        inputParams= self.getInput()

        try:
            Products.create(
                name = inputParams['name'],
                description = self.htmlunquote(inputParams['desc']),
                price1 = inputParams['price1'],
                price2 = inputParams['price2'],
                category = int(inputParams['category']),
                diameter = inputParams['diameter'],
                type = int(inputParams['type']),
            )  
        except Exception, e:
            return self.error(msg = '新增失败: %s' % e, url=self.makeUrl('/admin/products/list'))

        return self.success('新增成功', url=self.makeUrl('/admin/products/list'))
