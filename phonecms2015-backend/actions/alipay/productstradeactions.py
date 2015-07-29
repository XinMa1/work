# -*- coding: utf-8 -*-
#coding=utf-8

from actions.alipay.referer import indexAction as baseAlipayActions
from models.products import Products
from models.product_payments import ProductPayments

class productstradeActions(baseAlipayActions):
    def __init__(self):
        baseAlipayActions.__init__(self)

    def _get_trade_info(self, inputs, from_mobile):
        try:
            product = Products.get(Products.id == inputs.get("id",0))   
            total_fee = product.discount     
            count = int(inputs.get("count", 0))
            total_fee = total_fee*count 
        except Exception, e:
            raise e

        info = {
            "product_id": product.id,
            "total_fee": total_fee,
            "subject": product.name,
            "notify_url" : self._make_url('/alipay/productstradeactions/mobilenotify'),
            "body": "None"
        }
        return info

    def _save_trade_relationship(self, trade_id, trade_info):
        try:
            ProductPayments.create(
                product = trade_info["product_id"],
                transaction = trade_id
            )
        except Exception, e:
            pass
