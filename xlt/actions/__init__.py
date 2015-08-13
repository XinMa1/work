# -*- coding: utf-8 -*-
#coding=utf-8

import config
from log import log

import actions.admin
import actions.index
import actions.wap

#Mandatory urls
urls = [
    '/admin',               actions.admin.indexAction,
    '/admin/login',         actions.admin.login.indexAction,
    '/admin/login/(.*)',    actions.admin.login.refererAction,
    '/admin/logout',        actions.admin.logout.indexAction,
    '/admin/logout/(.*)',   actions.admin.logout.refererAction,
    '/admin/install',       actions.admin.install.indexAction,
    '/admin/install/(.*)',  actions.admin.install.refererAction,
    '/',                    actions.index.indexAction,
    '/admin/categories',        actions.admin.categories.indexAction,
    '/admin/categories/(.*)',   actions.admin.categories.refererAction, 
    '/admin/images',        actions.admin.images.indexAction,
    '/admin/images/(.*)',   actions.admin.images.refererAction, 
    '/admin/upload',        actions.admin.upload.indexAction,
    '/admin/upload/(.*)',   actions.admin.upload.refererAction, 
    '/admin/news',        actions.admin.news.indexAction,
    '/admin/news/(.*)',   actions.admin.news.refererAction, 
    '/admin/products',        actions.admin.products.indexAction,
    '/admin/products/(.*)',   actions.admin.products.refererAction, 
    '/admin/users',        actions.admin.users.indexAction,
    '/admin/users/(.*)',   actions.admin.users.refererAction, 
    '/admin/contacts',        actions.admin.contacts.indexAction,
    '/admin/contacts/(.*)',   actions.admin.contacts.refererAction, 
    '/admin/orders',        actions.admin.orders.indexAction,
    '/admin/orders/(.*)',   actions.admin.orders.refererAction, 
    '/admin/notifications',        actions.admin.notifications.indexAction,
    '/admin/notifications/(.*)',   actions.admin.notifications.refererAction,
    '/admin/accountings',        actions.admin.accountings.indexAction,
    '/admin/accountings/(.*)',   actions.admin.accountings.refererAction, 
    '/wap/(.*)',            actions.wap.refererAction,
]

if config.DEBUG: log.debug('Webpy url mapping: %s' % str(urls));
