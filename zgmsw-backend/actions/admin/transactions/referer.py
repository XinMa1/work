## -*- coding: utf-8 -*-
#coding=utf-8

import web
import os
import config
from actions.admin.base import adminAction
from models.course_payments import CoursePayments
from models.group_payments import GroupPayments
from models.users import Users
from models.transactions import Transactions
from models.transactions import TransactionStatus

'''
Admin controller: producing transcaction administration views.
'''
class refererAction(adminAction):
    def __init__(self):
        adminAction.__init__(self)


    def GET(self, name):
        if name == 'grouppaymentslist':
            return self.group_list()
        if name == 'coursepaymentslist':
            return self.course_list()

        return self.notFound()


    def group_list(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE
        offset= (page-1)*count if page > 0 else 0

        render_payments_info = []
        paymentsList = GroupPayments().select().order_by(GroupPayments.id.desc())
        pageString = self.getPageStr('/admin/transactions/grouppaymentslist', page, count, paymentsList.count())
        payments = paymentsList.paginate(page, config.COUNT_PER_PAGE)
        for payment in payments:
            payment_info = {
                "id": payment.id,
                "remark": payment.remark,
                "created_time": payment.created_time,
                "type": payment.type,
                "pay_time": "N/A",
                "group_name": payment.group,
                "total_fee": "",
                "owner":"",
                "trade_status":"未知",
            }
            if payment.transaction:
                transaction = payment.transaction
                payment_info["trade_status"] = TransactionStatus.statusName(
                                                    transaction.trade_status)
                payment_info["total_fee"] = transaction.total_price
                if transaction.trade_status == TransactionStatus.STATUS_COMPLETE:
                    payment_info["pay_time"] = transaction.last_modified_time
                if transaction.owner:
                    payment_info["owner"] = transaction.owner.name
                else:
                    payment_info["owner"] = transaction.owner
            if payment.group:
                payment_info["group_name"] = payment.group.name
            render_payments_info.append(payment_info)
        self.privData['PAYMENTS_LIST'] = render_payments_info
        self.privData['PAGE_STRING'] = pageString
        return self.display('grouppaymentsList')

    def course_list(self):
        inputParams = self.getInput()
        page = int(inputParams['page']) if inputParams.has_key('page') else 1
        count = config.COUNT_PER_PAGE
        offset= (page-1)*count if page > 0 else 0

        render_payments_info = []
        paymentsList = CoursePayments().select().order_by(CoursePayments.id.desc())
        pageString = self.getPageStr('/admin/transactions/coursepaymentslist', page, count, paymentsList.count())
        payments = paymentsList.paginate(page, config.COUNT_PER_PAGE)
        for payment in payments:
            payment_info = {
                "id": payment.id,
                "remark": payment.remark,
                "created_time": payment.created_time,
                "pay_time": "N/A",
                "course_name": payment.course,
                "total_fee": "",
                "owner":"",
                "trade_status":"未知",
            }
            if payment.transaction:
                transaction = payment.transaction
                payment_info["trade_status"] = TransactionStatus.statusName(
                                                    transaction.trade_status)
                payment_info["total_fee"] = transaction.total_price
                if transaction.trade_status == TransactionStatus.STATUS_COMPLETE:
                    payment_info["pay_time"] = transaction.last_modified_time
                if transaction.owner:
                    payment_info["owner"] = transaction.owner.name
                else:
                    payment_info["owner"] = transaction.owner
            if payment.course:
                payment_info["course_name"] = payment.course.name
            render_payments_info.append(payment_info)
        self.privData['PAYMENTS_LIST'] = render_payments_info
        self.privData['PAGE_STRING'] = pageString
        return self.display('coursepaymentsList')
