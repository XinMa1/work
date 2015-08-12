# -*- coding: utf-8 -*-
#coding=utf-8

import web
import os
import config
from actions.admin.base import adminAction
from dbinit import dbinit

'''
User controller: producing install views.
'''
class refererAction(adminAction):
    def __init__(self):
        adminAction.__init__(self, chkInstall=False)
        if not self.isAdmin():
            return self.error(msg = '权限不足!')

        self.sessions_dir = os.path.join(config.DATA_DIR, 'sessions')
        self.upload_dir = config.UPLOAD_DIR
        self.temp_dir = os.path.join(self.upload_dir, 'temp')
        self.video_dir = os.path.join(self.upload_dir, 'video')
        self.audio_dir = os.path.join(self.upload_dir, 'audio')
        self.image_dir = os.path.join(self.upload_dir, 'image')
    
    def install(self):
        try:
            required_dirs = (
                self.sessions_dir,
                self.upload_dir,
                self.temp_dir,
                self.video_dir,
                self.audio_dir,
                self.image_dir
            )

            for d in [d for d in required_dirs if not os.path.exists(d)]:
                os.makedirs(d)

            dbinitObj = dbinit()
            return self.success(msg = '系统安装成功.', url=self.makeUrl('/admin'))
        except Exception, e:
            return self.error(msg = '系统安装失败：%s' % e)

    def upgrade(self):
        return self.success(msg = '系统升级成功.', url=self.makeUrl('/admin'))

    def GET(self, name):
        if name == 'install':
            return self.install()
        elif name == 'upgrade':
            return self.upgrade()

        return self.notFound()
