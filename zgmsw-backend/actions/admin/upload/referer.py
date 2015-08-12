# -*- coding: utf-8 -*-
#coding=utf-8

import web
import config
import cgi
import os

from actions.admin.base import adminAction
from uploadmgr import httpUploadedFile
from models.images import Images
from models.categories import Categories


class refererAction(adminAction):
    def __init__(self, name = '上传文件'):
        adminAction.__init__(self, name)


    def POST(self, name):
        cgi.maxlen = int(config.MAX_UPLOAD_FILE_SIZE) * 1024 * 1024 # 2MB
        try:
            i = web.input(file={})
        except ValueError:
            return self.error(msg = '文件最大尺寸不能超过2M!')

        if name == 'file':
            return self.saveFile()
        elif name == 'image':
            return self.saveImage()
        elif name == 'image_default':
            return self.saveImageDefault()
        else:
            return self.notFound()

    
    def recordImage(self, f):
        import base64
        inputs = web.input()
        try: 
            iw = int(inputs['image_width'])
            ih = int(inputs['image_height'])
        except Exception, e:
            iw = config.IMAGE_XRES
            ih = config.IMAGE_YRES
        from imaging import imaging
        im = imaging(f.target())

        tmpfile = f.target() + ".tmp"
        data = im.resize(iw, ih) 
        file(tmpfile, 'w').write(data)
        os.unlink(f.target())
        os.rename(tmpfile, f.target())

        try:
            tw = int(inputs['thumbnail_width'])
            th = int(inputs['thumbnail_height'])
        except Exception, e:
            tw = config.THUMBNAIL_XRES
            th = config.THUMBNAIL_YRES

        blob = im.resize(tw, th)

        try:
            Images().create(
                uuid =  f.uuid(),
                description = self.htmlunquote(self.desc),
                album = self.album,
                owner = self.owner,
                thumbnail = base64.b64encode(buffer(blob))
            )
        except Exception, e:
            return 0
        return 1
   
    def saveFile(self):
        inputParams = web.input()
        if inputParams.has_key('file') and not inputParams['file']:
            return self.error(msg = '未指定文件')

        f = None

        try: 
            self.desc = inputParams['desc']
            self.album = int(inputParams['album'])
            self.owner = self.getUserId()
            self.ref = inputParams['ref'] if inputParams.has_key('ref') else None

            f = httpUploadedFile(inputParams.file)
            if f.mimetype().startswith('image'):
                c = self.recordImage(f)
                self.privData['text'] = self.imageUrl(c.lastrowid)
            else:
                return self.error(msg = '未知的文件类型')
        except Exception, e:
            if f and os.path.exists(f.target()):
                os.unlink(f.target())
            return self.error(msg = '保存对象失败: %s' % e)

        return self.display('copyText')

    def saveImage(self):
        inputParams = web.input()
        if inputParams.has_key('file') and not inputParams['file']:
            return self.error(msg = '未指定文件')

        f = None

        try:
            self.desc = inputParams['desc']
            self.ref = inputParams['ref'] 
            self.album = int(inputParams['album'])
            self.owner = int(inputParams['owner'])
            f = httpUploadedFile(inputParams.file)
            if f.mimetype() != 'image/jpeg':
                os.unlink(f.target())
                return self.error(msg='上传失败')
            self.recordImage(f)
        except Exception, e:
            if f and os.path.exists(f.target()):
                os.unlink(f.target())
            return self.error(msg='上传失败: %s' % e)
            
        return self.back(msg='上传成功')

    def saveImageDefault(self):
        inputParams = web.input()
        if inputParams.has_key('file') and not inputParams['file']:
            return self.error(msg = '未指定文件')

        f = None
        try:
            self.owner = 1
            self.desc = 'the image upload by default'
            self.ref = ''
            self.album = 1

            f = httpUploadedFile(inputParams.file)
            if f.mimetype() != 'image/jpeg':
                os.unlink(f.target())
                return self.error(msg='上传失败')
            if f.mimetype() == 'image/jpeg':
                self.recordImage(f)
        except Exception, e:
            if f and os.path.exists(f.target()):
                os.unlink(f.target())
            return self.error(msg='上传失败')

        return self.back(msg='上传成功')


