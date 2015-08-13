#!/usr/bin/env python
# -*- coding: utf-8 -*-
#coding=utf-8

import web
import actions
from peewee import *
from models.base import db


if __name__ == "__main__":
    theApp = web.application(actions.urls, globals())
    web.config.session_parameters['cookie_name'] = 'webpycms_sid'
    web.config.session_parameters['cookie_domain'] = None
    web.config.session_parameters['timeout'] = 86400,
    web.config.session_parameters['ignore_expiry'] = True
    web.config.session_parameters['ignore_change_ip'] = True
    web.config.session_parameters['secret_key'] = 'JJIEhi323rioes34hafwaj2'
    web.config.session_parameters['expired_message'] = 'Session expired'
    session = web.session.Session(theApp, web.session.DiskStore('data/sessions'), initializer={'login': False})
    def session_hook():
        web.ctx.session = session
    theApp.add_processor(web.loadhook(session_hook))
    def connection_processor(handler):
        db.connect()
        try:
            return handler()
        finally:
            if not db.is_closed():
                db.close()

    theApp.add_processor(connection_processor)

    theApp.run()
