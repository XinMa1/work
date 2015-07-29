# -*- coding: utf-8 -*-
#coding=utf-8

import base64
import datetime
import os
import pycurl
import re
import sys
import StringIO
import urllib
import uuid

from OpenSSL.crypto import load_privatekey, FILETYPE_PEM, sign
from M2Crypto import BIO, RSA, EVP

import config
from actions.alipay.base import alipayAction
from models.transactions import Transactions
from models.transactions import TransactionStatus
from models.users import Users

'''
AliPay controller
'''
class indexAction(alipayAction):
    def __init__(self):
        alipayAction.__init__(self)
        self.alipay_config = {
            'partner': config.ALIPAY_PARTNER,
            'key': config.ALIPAY_KEY,
            'private_key_path': config.ALIPAY_MOBILE_PRIVATE_KEY,
            'ali_mobile_public_key_path': config.ALIPAY_MOBILE_PUBLIC_KEY,
            'sign_type': '0001',
            'input_charset': 'utf-8',
            'cacert': config.ALIPAY_CACERT,
            'transport': 'http',
        }

        self.gateway_url = 'http://wappaygw.alipay.com/service/rest.htm?_input_charset='+self.alipay_config['input_charset']
        self.seller_email = config.ALIPAY_SELLER_EMAIL

    def GET(self, name):
        if name == 'payfrommui':
            return self.pay_from_mui()
        return self.notFound()

    def POST(self, name):
        if name == 'mobilenotify':
            return self.mobilenotify()
        return self.notFound()

    def __make_url(self, url, params={}):
        return "%s%s" % (config.WEB_URL,self.makeUrl(url, params))

    def _make_url(self, url, params={}):
        return self.__make_url(url, params)

    def pay_from_mui(self):
        inputs = self.getInput()
        trade_info = {}
        try:
            # this will raise an exception if user not found!
            try:
                user = Users.get(Users.token == inputs.get('token','illegal_token'))
            except Exception as e:
                return self.forbidden()

            trade_info = self._get_trade_info(inputs, True)

            trade_no = uuid.uuid4().hex
            self.__save_trade(trade_no, trade_info["total_fee"], user.id, TransactionStatus.STATUS_NONE)
            #MOCK user.id == 1
            #self.__save_trade(trade_no, 1, TransactionStatus.STATUS_NONE)
            condition={'tradeID': trade_no}
            trade = Transactions.get(Transactions.trade_id == trade_no)
            self._save_trade_relationship(trade.id, trade_info)
            #print("trade info is %s\n", trade_info)
           
            para = [
                ("service" , "mobile.securitypay.pay"),
                ("partner" , self.alipay_config['partner']),
                ("_input_charset", self.alipay_config['input_charset']),
                ("out_trade_no", trade_no),
                ("subject", trade_info["subject"]),
                ("payment_type", "1"),
                ("seller_id", self.seller_email),
                ("total_fee", trade_info["total_fee"]),
                ("body", trade_info.get("body", "None")), #不能为空,即使是空字符串也不行! TODO
                ("notify_url", trade_info["notify_url"]),
                #"show_url": ""
            ]


            prestr = "&".join(["%s=\"%s\"" % (key,str(val)) for key,val in para])
            sign = urllib.urlencode({"sign":self.__rsa_sign(prestr, self.alipay_config['private_key_path'])})
            split_sign = sign.split("=")
            sign = "=".join(["sign","\"%s\"" % split_sign[1]])
            
            ret="%s&%s&sign_type=\"RSA\"" % (prestr, str(sign))
            return ret

        except Exception as e:
            return self.error()

    """
    return keys: subject,body,notify_url,total_fee
    """
    def _get_trade_info(self, inputs, from_mobile):
        raise Exception("No implementation for _get_trade_info method")

    def _save_trade_relationship(self, trade_id, trade_info):
        raise Exception("No implementation for _save_trade_relationship method")
    

    def mobilenotify(self):
        inputs = self.getInput()
        verify_result = self.__verify_mobile_notify_result(inputs)
        if(verify_result):
            out_trade_no = inputs.get("out_trade_no", "")
            trade_no = inputs.get("trade_no", "")
            trade_status = inputs.get("trade_status", "")
            if trade_status == 'TRADE_FINISHED' or trade_status == 'TRADE_SUCCESS' or trade_status == 'WAIT_BUYER_PAY':
                trade_record = Transactions.get(Transactions.trade_id == out_trade_no)
                if trade_record:
                    trade_record.alipay_trade_id = trade_no
                    trade_record.last_modified_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    trade_record.description = str(inputs)
                    if trade_status == 'WAIT_BUYER_PAY':
                        trade_record.trade_status = TransactionStatus.STATUS_WAITPAY
                    else:
                        trade_record.trade_status = TransactionStatus.STATUS_COMPLETE
                    trade_record.save()
                else:
                    print('[IN MOBILE Notify]交易号%s不存在'%out_trade_no)
            else:
                print('[IN MOBILE Notify]交易信息非法:%s' % trade_status)
        else:
            print('[IN MOBILLE Notify]Verify失败:%s' % inputs)


    def __verify_mobile_notify_result(self, inputs):
        try:
            if len(inputs) == 0:
                return False
            else:
                para_filter = self.__para_filter(inputs);
                para_sort_list = sorted(para_filter.items(), key=lambda d:d[0])
                prestr = "&".join(["%s=%s" % (key,val) for \
                          key,val in para_sort_list])

                is_sign = False
                if self.alipay_config['sign_type'] == '0001':
                    is_sign=self.__rsa_verify(prestr, inputs['sign'], self.alipay_config['ali_mobile_public_key_path'])

                response_text = 'true'
                notify_id = inputs.get("notify_id", "")
                if notify_id:
                    response_text = self.__get_notify_response(notify_id)
                return True if is_sign and re.search('true$', response_text, re.I) else False
        except Exception as e:
            print("verify mobile notify result exception: %s" % e)
            return False


    def __get_notify_response(self, notify_id):
        transport = self.alipay_config['transport'].lower()
        partner = self.alipay_config['partner']
        if transport == 'https':
            verify_url = 'https://mapi.alipay.com/gateway.do?service=notify_verify&partner=%s&notify_id=%s' % (partner, notify_id)
        else:
            verify_url = 'http://notify.alipay.com/trade/notify_query.do?partner=%s&notify_id=%s' % (partner, str(notify_id))
        return self.__get_http_response_get(verify_url, self.alipay_config['cacert'])


    def __save_trade(self, trade_no, total_fee, owner, status):
        if status > TransactionStatus.STATUS_ERROR or \
                status < TransactionStatus.STATUS_NONE:
            raise "Illegal trade status"

        Transactions.create(trade_id = trade_no, owner = owner, total_price=total_fee,
                            trade_status = status)


    def __get_http_response_get(self, url, cacert_url):
        response = StringIO.StringIO()
        curl = pycurl.Curl()
        curl.setopt(pycurl.URL, url)
        curl.setopt(pycurl.HEADER, 0 )#过滤HTTP头
        curl.setopt(pycurl.SSL_VERIFYPEER, True)#SSL证书认证
        curl.setopt(pycurl.SSL_VERIFYHOST, 2)#严格认证
        curl.setopt(pycurl.CAINFO,self.alipay_config['cacert'])#证书地址
        curl.setopt(pycurl.WRITEFUNCTION, response.write)
        curl.perform()
        responseText = response.getvalue()
        curl.close()

        return responseText;

    
    '''
     除去数组中的空值和签名参数
     @param $para 签名参数组
     return 去掉空值与签名参数后的新签名参数组
    '''
    def __para_filter(self, para):
        return dict([(key,val) for key,val in para.iteritems() if \
            key != "sign" and key != "sign_type" and val != ""])


    '''
     RSA签名
     @param $data 待签名数据
     @param $private_key_path private_key path
     return 签名结果
    '''
    def __rsa_sign(self, data, private_key_path):
        key = load_privatekey(FILETYPE_PEM, open(private_key_path).read())
        return base64.b64encode(sign(key, data, 'sha1'))


    def __rsa_verify(self, string, sign, public_key_path):
        #print("string is %s, sign is %s, key: %s\n" % (string, sign, public_key_path))
        bio = BIO.MemoryBuffer(open(public_key_path).read())
        rsa = RSA.load_pub_key_bio(bio)
        pubkey = EVP.PKey()
        pubkey.assign_rsa(rsa)
        pubkey.reset_context(md='sha1')
        pubkey.verify_init()
        pubkey.verify_update(str(string))
        ret=pubkey.verify_final(base64.b64decode(str(sign)))
        #return True if pubkey.verify_final(base64.b64decode(sign)) == 1 else False
        return True if ret == 1 else False
