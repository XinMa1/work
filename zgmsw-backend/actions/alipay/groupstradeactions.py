# -*- coding: utf-8 -*-
#coding=utf-8

from actions.alipay.referer import indexAction as baseAlipayActions
from models.groups import Groups
from models.group_payments import GroupPayments

class groupstradeActions(baseAlipayActions):
    def __init__(self):
        baseAlipayActions.__init__(self)

    def _get_trade_info(self, inputs, from_mobile):
        try:
            group = Groups.get(Groups.id == inputs.get("id",0))
        except Exception, e:
            raise e

        type = inputs.get("type", 0)
        total_fee = float(group.price_remote_service) if type else float(group.price_home_service)
        count = int(inputs.get("count", 0))
        total_fee = total_fee*count

        info = {
            "group_id": group.id,
            "total_fee": total_fee,
            "subject": group.name,
            "notify_url" : self._make_url('/alipay/groupstradeactions/mobilenotify'),
            #"body": self.subText(self.htmlunquote(group.description), 0, 32),
            "body": "None",
            "type": type,
        }
        return info

    def _save_trade_relationship(self, trade_id, trade_info):
        try:
            GroupPayments.create(
                group = trade_info["group_id"],
                transaction = trade_id,
                type = trade_info["type"]
            )
        except Exception, e:
            pass
