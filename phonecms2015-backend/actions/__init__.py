# -*- coding: utf-8 -*-
#coding=utf-8

import config
from log import log

import actions.admin
import actions.index
import actions.api
import actions.alipay

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
    '/admin/albums',        actions.admin.albums.indexAction,
    '/admin/albums/(.*)',   actions.admin.albums.refererAction,
    '/admin/groups',        actions.admin.groups.indexAction,
    '/admin/groups/(.*)',   actions.admin.groups.refererAction,
    '/admin/products',       actions.admin.products.indexAction,
    '/admin/products/(.*)',  actions.admin.products.refererAction,
    '/admin/categories',       actions.admin.categories.indexAction,
    '/admin/categories/(.*)',  actions.admin.categories.refererAction,
    '/admin/images',        actions.admin.images.indexAction,
    '/admin/images/(.*)',   actions.admin.images.refererAction,
    '/admin/upload',        actions.admin.upload.indexAction,
    '/admin/upload/(.*)',   actions.admin.upload.refererAction,
    '/admin/users',         actions.admin.users.indexAction,
    '/admin/users/(.*)',    actions.admin.users.refererAction,
    '/admin/articles',         actions.admin.articles.indexAction,
    '/admin/articles/(.*)',    actions.admin.articles.refererAction,
    '/admin/questions',         actions.admin.questions.indexAction,
    '/admin/questions/(.*)',    actions.admin.questions.refererAction,
    '/admin/transactions',         actions.admin.transactions.indexAction,
    '/admin/transactions/(.*)',    actions.admin.transactions.refererAction,
    '/admin/chatrooms',         actions.admin.chatrooms.indexAction,
    '/admin/chatrooms/(.*)',    actions.admin.chatrooms.refererAction,
      
    '/api/(.*)',            actions.api.apiActions,
    '/alipay/productstradeactions/(.*)',   actions.alipay.productstradeActions,
    '/alipay/groupstradeactions/(.*)',   actions.alipay.groupstradeActions,
]

if config.DEBUG: log.debug('Webpy url mapping: %s' % str(urls));
