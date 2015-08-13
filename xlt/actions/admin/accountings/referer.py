# -*- coding: utf-8 -*-
#coding=utf-8

import config
from actions.admin.base import adminAction
from models.users import Users
from models.accountings import Accountings
from models.account_incommings import AccountIncommings
from models.account_outgoings import AccountOutgoings

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
        elif name == 'incommings':
            return self.incommings()
        elif name == 'add_incomming':
            return self.add_incomming()
        elif name == 'delete_incomming':
            return self.delete_incomming()
        elif name == 'edit_incomming':
            return self.edit_incomming()
        elif name == 'outgoings':
            return self.outgoings()
        elif name == 'add_outgoing':
            return self.add_outgoings()
        elif name == 'delete_outgoing':
            return self.delete_outgoing()
        elif name == 'edit_outgoing':
            return self.edit_outgoing()
        else:
            return self.notFound()

    def POST(self, name):
        if name == 'save':
            return self.save()
        elif name == 'search':
            return self.search() 
        elif name == 'modify':
            return self.modify()
        elif name == 'incoming_save':
            return self.incoming_save()
        elif name == 'incomming_update':
            return self.incomming_update()
        elif name == 'outgoing_save':
            return self.outgoing_save()
        elif name == 'outgoing_update':
            return self.outgoing_update()
        else:
            return self.notFound()

    def list(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE

        accountingsList = Accountings.select().order_by(Accountings.id.desc())
        pageString = self.getPageStr(self.makeUrl('/admin/accountings/list'), page, count, accountingsList.count())
        self.privData['ACCOUNTINGS_LIST'] = accountingsList.paginate(page, count)
        self.privData['PAGE_STRING'] = pageString
        return self.display('accountingsList')

    def delete(self):
        inputParams = self.getInput()

        try:
            a = Accountings.get(Accountings.id == int(inputParams['id']))
            a.delete_instance()
        except Exception, e:
            return self.error(msg = '删除失败: %s' % e, url=self.makeUrl('/admin/accountings/list'))
    
        return self.success(msg='删除成功', url=self.makeUrl('/admin/accountings/list'))

     
    def search(self):
        inputParams = self.getInput()
        keywords = inputParams['keywords'].strip().lower() if inputParams.has_key('keywords') else ''
        
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE

        accountingsList = Accountings.select().where(Accountings.name.contains(keywords)).order_by(Accountings.id.desc())
        pageString = self.getPageStr(self.makeUrl('/admin/accountings/list'), page, count, accountingsList.count())
        self.privData['ACCOUNTINGS_LIST'] = accountingsList.paginate(page, count)
        self.privData['PAGE_STRING'] = pageString
        return self.display('accountingsList')

        
    def add(self):
        userList = Users.select()
        self.privData['USERS_LIST'] = userList
        return self.display('accountingAdd')

    def modify(self):
        inputParams= self.getInput()
         
        try:
            accounting_id = int(inputParams['id'])
            accounting = Accountings.get(Accountings.id == accounting_id)
            accounting.status = int(inputParams['status'])
            accounting.owner = inputParams['owner']
            accounting.symwjzje = inputParams['symwjzje']
            accounting.byfhhj = inputParams['byfhhj']
            accounting.bydzhj = inputParams['bydzhj']
            accounting.ymjc = inputParams['ymjc']
            accounting.byywlr = inputParams['byywlr']
            accounting.bykp = inputParams['bykp']
            accounting.byj = inputParams['byj']
            accounting.byk = inputParams['byk']
            accounting.bnfhlj = inputParams['bnfhlj']
            accounting.bndzlj = inputParams['bndzlj']        
            accounting.description = inputParams['content']
            accounting.save()
        except Exception, e:
            return self.error(msg = '修改失败: %s' % e, url=self.makeUrl('/admin/accountings/list'))

        return self.success('修改成功', url=self.makeUrl('/admin/accountings/list'))

    def edit(self):
        inputParams = self.getInput()
        accounting = Accountings.get(Accountings.id == int(inputParams['id']))
        userList = Users.select()
        self.privData['USERS_LIST'] = userList
        self.privData['ACCOUNTING'] =  accounting
        return self.display('accountingEdit')

    def edit_incomming(self):
        inputParams = self.getInput()
        accountingID = inputParams['accountid']
        inoroutID = inputParams['id']
        inorout = AccountIncommings.get(AccountIncommings.id == int(inputParams['id']))
        self.privData['INOROUT'] = inorout
        self.privData['ACCOUNTING_ID'] =  accountingID
        return self.display('incommingEdit')


    def delete_incomming(self):
        inputParams = self.getInput()

        try:
            accountID = int(inputParams['accountid'])
            a = AccountIncommings.get(AccountIncommings.id == int(inputParams['id']))
            a.delete_instance()
        except Exception, e:
            return self.error(msg = '删除失败: %s' % e, url=self.makeUrl('/admin/accountings/list'))

        return self.success(msg='删除成功', url=self.makeUrl('/admin/accountings/incommings', {'accounting': accountID}))     

    def incommings(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE
        accounting = Accountings.get(Accountings.id == int(inputParams['accounting']))
        incommingsList = AccountIncommings.select().where(AccountIncommings.accounting==accounting).order_by(AccountIncommings.id.desc())
        pageString = self.getPageStr(self.makeUrl('/admin/accountings/incommings', {'accounting': accounting.id}), page, count, incommingsList.count())
        self.privData['INCOMMINGS_LIST'] = incommingsList.paginate(page, count)
        self.privData['ACCOUNTING'] =  accounting
        self.privData['PAGE_STRING'] = pageString
        return self.display('incommingsList')
    
    def add_incomming(self):
        inputParams = self.getInput()
        accountingID = inputParams['id']
        self.privData['ACCOUNTING_ID'] =  accountingID
        return self.display('incommingAdd')


    def incoming_save(self):
        userInput = self.getInput()
        try:
            accountID = userInput['id']
            account = Accountings.get(Accountings.id == accountID)
            AccountIncommings.create(
                origin  = userInput['name'],
                money = userInput['money'],
                accounting = account,
                description = userInput['content'],
            )
        except Exception, e:
            return self.error(msg = '新增失败: %s' % e, url=self.makeUrl('/admin/accountings/list'))

        return self.success('新增成功', url=self.makeUrl('/admin/accountings/incommings', {'accounting': accountID}))

    def incomming_update(self):
        inputParams = self.getInput()
        try:
            accountID = int(inputParams['accountID'])
            inorout_id = int(inputParams['id'])
            inorout = AccountIncommings.get(AccountIncommings.id == inorout_id)
            inorout.money = inputParams['money']
            inorout.origin = inputParams['name']
            inorout.description = inputParams['content']
            inorout.save()
        except Exception, e:
            return self.error(msg = '修改失败: %s' % e, url=self.makeUrl('/admin/accountings/incommings', {'accounting': accountID}))
        return self.success('修改成功', url=self.makeUrl('/admin/accountings/incommings', {'accounting': accountID}))



    def outgoing_save(self):
        userInput = self.getInput()
        accountID = userInput['id']
        account = Accountings.get(Accountings.id == accountID)
        try:
            AccountOutgoings.create(
                money = userInput['money'],
                accounting = account,
                count = userInput['count'],
                description = userInput['content']
            )
        except Exception, e:
            return self.error(msg = '新增失败: %s' % e, url=self.makeUrl('/admin/accountings/outgoings',{'accounting': accountID}))
        return self.success('新增成功', url=self.makeUrl('/admin/accountings/outgoings', {'accounting': accountID}))

    def add_outgoings(self):
        inputParams = self.getInput()
        accountingID = inputParams['id']
        self.privData['ACCOUNTING_ID'] =  accountingID
        return self.display('outgoingAdd')

    def add_incomming(self):
        inputParams = self.getInput()
        accountingID = inputParams['id']
        self.privData['ACCOUNTING_ID'] =  accountingID
        return self.display('incommingAdd')

    def outgoings(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE
        accountID = int(inputParams['accounting'])
        accounting = Accountings.get(Accountings.id == int(inputParams['accounting']))
        outgoingsList = AccountOutgoings.select().where(AccountOutgoings.accounting==accounting).order_by(AccountOutgoings.id.desc())
        pageString = self.getPageStr(self.makeUrl('/admin/accountings/outgoings', {'accounting': accounting.id}), page, count, outgoingsList.count())
        self.privData['OUTGOINGS_LIST'] = outgoingsList.paginate(page, count)
        self.privData['ACCOUNTING'] =  accounting
        self.privData['PAGE_STRING'] = pageString
        return self.display('outgoingsList')

    def edit_outgoing(self):
        inputParams = self.getInput()
        accountingID = inputParams['accountid']
        inoroutID = inputParams['id']
        inorout = AccountOutgoings.get(AccountOutgoings.id == int(inputParams['id']))
        self.privData['INOROUT'] = inorout
        self.privData['ACCOUNTING_ID'] =  accountingID
        return self.display('outgoingEdit')


    def outgoing_update(self):
        inputParams = self.getInput()
        try:
            accountID = int(inputParams['accountID'])
            inorout_id = int(inputParams['id'])
            inorout = AccountOutgoings.get(AccountOutgoings.id == inorout_id)
            inorout.money = inputParams['money']
            inorout.count = inputParams['count']
            inorout.description = inputParams['content']
            inorout.save()
        except Exception, e:
            return self.error(msg = '修改失败: %s' % e, url=self.makeUrl('/admin/accountings/outgoings', {'accounting': accountID}))
        return self.success('修改成功', url=self.makeUrl('/admin/accountings/outgoings', {'accounting': accountID}))

    def delete_outgoing(self):
        inputParams = self.getInput()

        try:
            accountID = int(inputParams['accountid'])
            a = AccountOutgoings.get(AccountOutgoings.id == int(inputParams['id']))
            a.delete_instance()
        except Exception, e:
            return self.error(msg = '删除失败: %s' % e, url=self.makeUrl('/admin/accountings/outgoings', {'accounting': accountID}))

        return self.success(msg='删除成功', url=self.makeUrl('/admin/accountings/outgoings', {'accounting': accountID}))


    def save(self):
        userInput = self.getInput()  
        try:
            Accountings.create(
                owner = userInput['owner'],
                bndzlj = userInput['bndzlj'],
                bnfhlj = userInput['bnfhlj'],
                byk = userInput['byk'],
                byj = userInput['byj'],
                bykp = userInput['bykp'],
                byywlr = userInput['byywlr'],
                ymjc = userInput['ymjc'],
                bydzhj = userInput['bydzhj'],
                byfhhj = userInput['byfhhj'],
                symwjzje = userInput['symwjzje'],
                description = userInput['content'],
            )          
        except Exception, e:
            return self.error(msg = '新增失败: %s' % e, url=self.makeUrl('/admin/accountings/list'))

        return self.success('新增成功', url=self.makeUrl('/admin/accountings/list'))
