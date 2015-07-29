# -*- coding: utf-8 -*-
#coding=utf-8
from xml.sax.saxutils import escape

from actions.alipay.referer import indexAction as baseAlipayActions
from models.courses import Courses
from models.course_payments import CoursePayments

class coursestradeActions(baseAlipayActions):
    def __init__(self):
        baseAlipayActions.__init__(self)

    def _get_trade_info(self, inputs, from_mobile):
        try:
            course = Courses.get(Courses.id == inputs.get("id",0))        
        except Exception, e:
            raise e

        info = {
            "course_id": course.id,
            "total_fee": course.discount,
            "subject": course.video_name,
            "notify_url" : self._make_url('/alipay/coursestradeactions/mobilenotify'),
            "body": "None",
        }
        return info

    def _save_trade_relationship(self, trade_id, trade_info):
        try:
            CoursePayments.create(
                course = trade_info["course_id"],
                transaction = trade_id
            )
        except Exception, e:
            pass
