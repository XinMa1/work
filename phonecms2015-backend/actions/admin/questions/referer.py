# -*- coding: utf-8 -*-
#coding=utf-8

import config
from actions.admin.base import adminAction
from models.questions import Questions
from models.answners import Answners
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
        elif name == 'answners':
            return self.answners()
        elif name == 'answnerAdd':
            return self.answnerAdd()
        elif name == 'answnerEdit':
            return self.answnerEdit()
        elif name == 'answnerDelete':
            return self.answnerDelete()
        elif name == 'detail':
            return self.detail()
        return self.notFound()

    def POST(self, name):
        if name == 'answnerSave':
            return self.answnerSave()
        elif name == 'answnerModify':
            return self.answnerModify()
        elif name == 'search':
            return self.search()
        elif name == 'answnersSearch':
            return self.answnersSearch() 
        else:
            return self.notFound()

    def list(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE

        questionsList = Questions.select()
        current_user = Users.get(Users.name == self.isLogin())
        if not self.isAdmin():
            questionsList = current_user.questions_owner
        questionsList = questionsList.order_by(Questions.id.desc())
        pageString = self.getPageStr(self.makeUrl('/admin/agents/list'), page, count, questionsList.count())

        self.privData['QUESTIONS_LIST'] = questionsList.paginate(page, count)
        self.privData['PAGE_STRING'] = pageString

        return self.display('questionsList')

    def detail(self):
        inputParams = self.getInput()
        qID = inputParams['id']
        question = Questions.get(Questions.id == qID)
        self.privData['QUESTION'] = question
        return self.display('questionDetail')

    def answnerAdd(self):
        inputParams = self.getInput()
        qID = inputParams['question']
        question = Questions.get(Questions.id == qID)
        
        current_user = Users.get(Users.name == self.isLogin())
        if not self.isAdmin() or question.group.owner != current_user:
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/questions/list'))
        
        self.privData['QUESTION'] = question

        return self.display('answnerAdd')
 
    def answnerEdit(self):
        inputParams = self.getInput()
        answner = Answners.get(Answners.id == inputParams['id'])

        current_user = Users.get(Users.name == self.isLogin())
        if not self.isAdmin() or answner.question.group.owner != current_user:
            return self.error(msg = '权限不足!', url=self.makeUrl('/admin/questions/list'))
        self.privData['ANSWNER'] = answner

        return self.display('answnerEdit')

   
    def answnerSave(self):
        userInput = self.getInput()
        try:
            qID = int(userInput['question'])
            question = Questions.get(Questions.id == qID)
            current_user = Users.get(Users.name == self.isLogin())
            if not self.isAdmin() or question.group.owner != current_user:
                return self.error(msg = '权限不足!', url=self.makeUrl('/admin/questions/answners', {'id': qID}))

            Answners.create(
                question = question,
                owner = current_user,
                content = userInput['content']
            )

        except Exception, e:
            return self.error(msg = '新增回答失败: %s' % e, url=self.makeUrl('/admin/questions/list'))

        return self.success('新增回答成功', url=self.makeUrl('/admin/questions/list'))

    def answnerModify(self):
        userInput = self.getInput()
        try:
            answner = Answners.get(Answners.id == int(userInput['id']))

            current_user = Users.get(Users.name == self.isLogin())
            if not self.isAdmin() or answner.question.group.owner != current_user:
                return self.error(msg = '权限不足!', url=self.makeUrl('/admin/questions/list'))

            answner.content = userInput['content']
            answner.save()
        except Exception, e:
            return self.error(msg = '修改回复失败: %s' % e, url=self.makeUrl('/admin/questions/list'))

        return self.success('修改回复成功', url=self.makeUrl('/admin/questions/list'))

    def answnerDelete(self):
        userInput = self.getInput()
        try:
            answner = Answners.get(Answners.id == int(userInput['id']))

            current_user = Users.get(Users.name == self.isLogin())
            if not self.isAdmin() or answner.question.group.owner != current_user:
                return self.error(msg = '权限不足!', url=self.makeUrl('/admin/questions/list'))

            answner.delete_instance()
        except Exception, e:
            return self.error(msg = '删除回复失败: %s' % e, url=self.makeUrl('/admin/questions/list'))

        return self.success('删除回复成功', url=self.makeUrl('/admin/questions/list'))

    def answners(self):
        inputParams = self.getInput()
        qID = inputParams['id']
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE
        question = Questions.get(Questions.id == qID)
        answnersList = Answners.select().where(Answners.question == qID)
        answnersList = answnersList.order_by(Answners.id.desc())
        pageString = self.getPageStr(self.makeUrl('/admin/answners/list', {'id': qID}), page, count, answnersList.count()) 
        self.privData['ANSWNERS_LIST'] = answnersList.paginate(page, count)
        self.privData['PAGE_STRING'] = pageString
        self.privData['QUESTION'] = question
        return self.display('answnersList')

    def delete(self):
        inputParams = self.getInput()

        try:
            current_user = Users.get(Users.name == self.isLogin())
            if  not self.isAdmin():
                return self.error(msg = '权限不足!', url=self.makeUrl('/admin/agents/list')) 
            question = Questionss.get(Questions.id == int(inputParams['id']))
            question.delete_instance()
        except Exception, e:
            return self.error(msg = '删除问题失败: %s' % e, url=self.makeUrl('/admin/questions/list'))
    
        return self.success(msg='删除问题成功', url=self.makeUrl('/admin/questions/list'))
    def search(self):
        inputParams = self.getInput()
        keywords = inputParams['keywords'].strip().lower() if inputParams.has_key('keywords') else ''
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE

        current_user = Users.get(Users.name == self.isLogin())
        questionsList = Questions.select().where(Questions.title.contains(keywords))
        if not self.isAdmin():
            questionsList = current_user.questions_owner
        questionsList = questionsList.order_by(Questions.id.desc())
        pageString = self.getPageStr(self.makeUrl('/admin/questions/list'), page, count, questionsList.count())

        self.privData['QUESTIONS_LIST'] = questionsList.paginate(page, count)
        self.privData['PAGE_STRING'] = pageString

        return self.display('questionsList')
    def answnersSearch(self):
        inputParams = self.getInput()
        keywords = inputParams['keywords'].strip().lower() if inputParams.has_key('keywords') else ''
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        qID = int(inputParams['qid'])
        count = config.COUNT_PER_PAGE
        question = Questions.get(Questions.id == qID)
        answnersList = Answners.select().where(Answners.question == qID and Answners.content.contains(keywords))
        answnersList = answnersList.order_by(Answners.id.desc())
        pageString = self.getPageStr(self.makeUrl('/admin/questions/answners', {'id': qID}), page, count, answnersList.count())
        self.privData['ANSWNERS_LIST'] = answnersList.paginate(page, count)
        self.privData['PAGE_STRING'] = pageString
        self.privData['QUESTION'] = question
        return self.display('answnersList')
