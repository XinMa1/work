# -*- coding: utf-8 -*-
#coding=utf-8

from actions.alipay.referer import indexAction as baseAlipayActions

class mocktradeActions(baseAlipayActions):
    def __init__(self):
        baseAlipayActions.__init__(self)

    def _get_trade_info(self, inputs, from_mobile):
        info = {
            "total_fee": 0.01,
            "subject": "ABCD",
            "notify_url" : self._make_url('/alipay/mocktradeactions/mobilenotify'),
            "body": "BODY",
        }
        return info

    def _save_trade_relationship(self, trade_id, trade_info):
        return
