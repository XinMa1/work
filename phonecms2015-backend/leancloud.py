# -*- coding: utf-8 -*-
#coding=utf-8

import json
import urllib2
import config

class Apis (object):
    __app_id = config.leancloud_app_id
    __app_key = config.leancloud_app_key

    __headers = {
        "X-AVOSCloud-Application-Id": __app_id,
        "X-AVOSCloud-Application-Key": __app_key,
        "Content-Type": "application/json",
    }

    def request_sms_code(self, phonenumber):
        url = "https://api.leancloud.cn/1.1/requestSmsCode"
        data = """
            {
                "mobilePhoneNumber": "%s"
            }
            """ % phonenumber

        try:
            req = urllib2.Request(url=url, data=data, headers=Apis.__headers)
            urllib2.urlopen(req)
            return True
        except Exception, e:
            return False

    def verify_sms_code(self, phonenumber, code):
        url = "https://api.leancloud.cn/1.1/verifySmsCode/%s" % code
        data = """
            {
                "mobilePhoneNumber": "%s"
            }
            """ % phonenumber

        try:
            req = urllib2.Request(url=url, data=data, headers=Apis.__headers)
            urllib2.urlopen(req)
            return True
        except Exception, e:
            print e
            return False


    def create_conversation(self, name, creator):
        url = "https://api.leancloud.cn/1.1/classes/_Conversation"
        data = """
            {
                "creator": "%s",
                "name":"%s",
                "m": ["%s"]
            }
            """ % (creator, name, creator)

        req = urllib2.Request(url=url, data=data, headers=Apis.__headers)
        resp = json.loads(urllib2.urlopen(req).read())
        return resp["objectId"]

    def remove_conversation(self, conv):
        url = "https://api.leancloud.cn/1.1/classes/_Conversation/%s" % conv
        req = urllib2.Request(url=url, headers=Apis.__headers)
        req.get_method = lambda: 'DELETE'
        resp = json.loads(urllib2.urlopen(req).read())
        return resp

    def add_to_conversation(self, conv, client):
        url = "https://api.leancloud.cn/1.1/classes/_Conversation/%s" % conv

        data = """
            {"m": {"__op":"AddUnique","objects":["%s"]}}
            """ % client

        req = urllib2.Request(url=url, data=data, headers=Apis.__headers)
        req.get_method = lambda: 'PUT'
        resp = json.loads(urllib2.urlopen(req).read())
        return resp

    def remove_from_conversation(self, conv, client):
        url = "https://api.leancloud.cn/1.1/classes/_Conversation/%s" % conv

        data = """
            {"m": {"__op":"Remove","objects":["%s"]}}
            """ % client

        req = urllib2.Request(url=url, data=data, headers=Apis.__headers)
        req.get_method = lambda: 'PUT'
        resp = json.loads(urllib2.urlopen(req).read())
        return resp

if __name__ == '__main__':
    #Apis().request_sms_code("18629551963")
    #Apis().verify_sms_code("17709185275", "964081")
    conv = Apis().create_conversation("测试聊天室", "管理员")
    print Apis().add_to_conversation(conv, "hluo2")
    print Apis().add_to_conversation(conv, "hluo1")
    print Apis().remove_from_conversation(conv, "hluo2")
    print Apis().remove_conversation(conv)
