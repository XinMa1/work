# -*- coding: utf-8 -*-
#coding=utf-8

import config
from actions.admin.base import adminAction
from models.news import News
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
        offset= (page-1)*count if page > 0 else 0

        newsList = News.select().order_by(News.id.desc())
        pageString = self.getPageStr(self.makeUrl('/admin/news/list'), page, count, newsList.count())
        self.privData['NEWS_LIST'] = newsList.paginate(offset, offset+count)
        self.privData['PAGE_STRING'] = pageString
        return self.display('newsList')

    def delete(self):
        inputParams = self.getInput()

        try:
            news = News.get(News.id == int(inputParams['id']))
            news.delete_instance()
        except Exception, e:
            return self.error(msg = '删除失败: %s' % e, url=self.makeUrl('/admin/news/list'))
    
        return self.success(msg='删除成功', url=self.makeUrl('/admin/news/list'))

     
    def search(self):
        inputParams = self.getInput()
        keywords = inputParams['keywords'].strip().lower() if inputParams.has_key('keywords') else ''
        
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE
        offset= (page-1)*count if page > 0 else 0

        newsList = News.select().where(News.name.contains(keywords)).order_by(News.id.desc())
        pageString = self.getPageStr(self.makeUrl('/admin/news/list'), page, count, newsList.count())
        self.privData['NEWS_LIST'] = newsList.paginate(offset, offset+count)
        self.privData['PAGE_STRING'] = pageString
        return self.display('newsList')

        
    def add(self):
        imagesList = Images().select()

        if not imagesList.count():
            return self.error(msg = '请创建至少一个图片!', url=self.makeUrl('/admin/images/list'))

        self.privData['IMAGES_LIST'] = imagesList
        self.privData['CURRENT_IMG'] = imagesList[0]
        self.privData['SUBMIT_NAME'] = "thumbnail"

        return self.display('newsAdd')

    def modify(self):
        inputParams= self.getInput()
         
        try:
            news_id = int(inputParams['id'])
            news = News().get(News.id == news_id)
            news.name = inputParams['name']
            news.content = inputParams['content']
            news.thumbnail = inputParams['thumbnail']
            news.save()
        except Exception, e:
            return self.error(msg = '修改失败: %s' % e, url=self.makeUrl('/admin/news/list'))

        return self.success('修改成功', url=self.makeUrl('/admin/news/list'))

    def edit(self):
        inputParams = self.getInput()
        newsID = int(inputParams['id'])
        news = News.get(News.id == newsID)
        self.privData['NEWS'] =   news

        imagesList = Images().select()
        if not imagesList.count():
            return self.error(msg = '请创建至少一个图片!', url=self.makeUrl('/admin/images/list'))


        self.privData['IMAGES_LIST'] = imagesList
        self.privData['CURRENT_IMG'] = news.thumbnail
        self.privData['SUBMIT_NAME'] = "thumbnail"

        return self.display('newsEdit')


    def save(self):
        userInput = self.getInput()  
        try:
            thumbnail = int(userInput['thumbnail']);
            News.create(
                name = userInput['name'],
                thumbnail = thumbnail,
                content = userInput['content']
            )
          
        except Exception, e:
            return self.error(msg = '新增失败: %s' % e, url=self.makeUrl('/admin/news/list'))

        return self.success('新增成功', url=self.makeUrl('/admin/news/list'))
