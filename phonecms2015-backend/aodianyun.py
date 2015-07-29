# -*- coding: utf-8 -*-
#coding=utf-8

import json
import urllib2
import config

class Apis (object):
    AccessID = config.aodianyun_access_id
    AccessKey = config.aodianyun_access_key
    __headers = {
        "Content-Type": "application/x-www-form-urlencoded",
    }

    def get_upload_vod_list(self):
        url = "http://openapi.aodianyun.com/v2/VOD.GetUploadVodList"
        data = """parameter={"access_id":"%s","access_key":"%s"}
            """ % (Apis.AccessID,Apis.AccessKey)
     
        req = urllib2.Request(url=url, data=data, headers=Apis.__headers)
        rsp = urllib2.urlopen(req)
        return json.loads(rsp.read())

if __name__ == '__main__':
    vods = Apis().get_upload_vod_list()
    for vod in vods["List"]:
        print vod
        print "title: %s" % vod["title"]
        print "url:   %s" % vod["url"]
        print "desc:  %s" % vod["desc"]
        print "case:  %s" % vod["case"]
        print "caseName:  %s" % vod["caseName"]
        print
