# -*- coding: utf-8 -*-
#coding=utf-8

import web
import os
import config
import hashlib
from actions.admin.base import adminAction
from models.users import Users
'''
Admin controller: producing login views.
'''
class refererAction(adminAction):
    def __init__(self):
        adminAction.__init__(self, chkLogin=False, chkInstall=False)


    def check(self):
        from web import form
        validList=(
            form.Textbox("username", form.regexp(r".{3,20}$", 'User name: 3-20 chars')),
            form.Password("password", form.regexp(r".{3,20}$", 'Password: 3-20 chars')),
        )

        if not self.validates(validList):
            return self.error(self.errorMessage)

        inputData = self.getInput()
        if config.ADMIN_USERNAME == inputData['username'] and config.ADMIN_PASSWORD == inputData['password']:
            self.setLogin(inputData['username'])
            return self.success(msg='管理员登陆成功', url=self.makeUrl('/admin'))
        else:
            if not self.isInstalled():
                return self.error(msg='用户登录失败, 系统未初始化!', url=self.makeUrl('/admin'))

            userName = inputData['username']
            password = hashlib.md5(inputData['password']).hexdigest()
            try:
                userObj = Users().select().where(Users.name == userName)
                if userObj.where(Users.name == userName, Users.password == password).exists() == False:
                    return self.error(msg='用户登录失败，请检查用户名和密码是否匹配', url=self.makeUrl('/admin'))
                self.setLogin(inputData['username'])
                return self.success(msg='用户登陆成功', url=self.makeUrl('/admin'))
            except  Users.DoesNotExist:
                return self.error(msg='用户登录失败，请检查用户名和密码是否匹配!', url=self.makeUrl('/admin'))

    def POST(self, name):
        if name == 'check':
            return self.check()
        else:
            return self.notFound()
