# -*- coding: utf-8 -*-
#coding=utf-8

import config
from actions.admin.base import adminAction
from models.categories import Categories

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

        categoriesList = Categories.select().order_by(Categories.id.desc())

        pageString = self.getPageStr(self.makeUrl('/admin/categories/list'), page, count, categoriesList.count())
        self.privData['CATEGORIES_LIST'] = categoriesList.paginate(page, count)
        self.privData['PAGE_STRING'] = pageString


        return self.display('categoriesList')

    def delete(self):
        inputParams = self.getInput()

        if int(inputParams['id']) == 1:
            return self.error(msg='不能删除系统预置分类', url=self.makeUrl('/admin/categories/list'))

        try:          
            category = Categories.get(Categories.id == int(inputParams['id']))
            category.delete_instance()
        except Exception, e:
            return self.error(msg = '分类删除失败: %s' % e, url=self.makeUrl('/admin/categories/list'))
    
        return self.success(msg='分类删除成功', url=self.makeUrl('/admin/categories/list'))

     
    def search(self):
        inputParams = self.getInput()
        keywords = inputParams['keywords'].strip().lower() if inputParams.has_key('keywords') else ''
        
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE

        categoriesList = Categories().select().where(Categories.name.contains(keywords)).order_by(Categories.id.desc())

        pageString = self.getPageStr(self.makeUrl('/admin/categories/list'), page, count, categoriesList.count())
        self.privData['CATEGORIES_LIST'] = categoriesList.paginate(page, count)
        self.privData['PAGE_STRING'] = pageString

        return self.display('categoriesList')

        
    def add(self):
        self.privData['CATEGORIES_LIST'] = Categories.select()
        return self.display('categoryAdd')

    def modify(self):
        inputParams = self.getInput()

        try:
            category_id = int(inputParams['id'])
            if category_id  == 1:
                return self.error(msg='不能编辑系统预置分类', url=self.makeUrl('/admin/categories/list'))
            category = Categories().get(Categories.id == category_id)
            category.name = inputParams['name']
            category.description = inputParams['desc']
            category.parent = int(inputParams['parent'])
            category.save()
        except Exception, e:
            return self.error(msg = '分类修改失败: %s' % e, url=self.makeUrl('/admin/categories/list'))

        return self.success('分类修改成功', url=self.makeUrl('/admin/categories/list'))

    def edit(self):
        inputParams = self.getInput()
        categoryID = int(inputParams['id'])
        categoriesObj = Categories.get(Categories.id == categoryID)
        self.privData['CATEGORY'] =  categoriesObj
        self.privData['CATEGORIES_LIST'] = Categories.select()
 
        return self.display('categoryEdit')


    def save(self):
        userInput = self.getInput()  
        try:
            Categories.create(
                name = userInput['name'],
                description = userInput['desc'],
                parent = int(userInput['parent'])
            )
          
        except Exception, e:
            return self.error(msg = '新增分类失败: %s' % e, url=self.makeUrl('/admin/categories/list'))

        return self.success('新增分类成功', url=self.makeUrl('/admin/categories/list'))
