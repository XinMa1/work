# -*- coding: utf-8 -*-
#coding=utf-8

import web
import json

from actions.base import jsonAction
from models.images import Images

'''
Ajax Actions: post and get ajax actions
'''

class ajaxAction(jsonAction):
    def __init__(self):
        jsonAction.__init__(self)
        self.region = web.ctx.session.region if hasattr(web.ctx.session, 'region') else None

    def GET(self, name):
        if name == 'images':
            return self.getImages()
        return self.notFound()

    def getImages(self):
        result = {'status': 0, 'data': [], 'msg': 'success'}
        userInput= self.getInput()
        album = userInput.get('album', -1)
        if album == -1:
            result['status'] = -1
            result['msg'] = '未指定专辑'
            return json.dumps(result)
        imagesList = Images().select().where(Images.album == album)
        for img in imagesList:
            result['data'].append({
                'id': img.id,
                'desc': img.description,
                'url': self.makeUrl('/admin/images/thumbnail',{'id': img.id}),
                'src': self.imageUrl(img.id),
                })
        return json.dumps(result)


