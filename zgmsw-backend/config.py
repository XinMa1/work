#!/usr/bin/env python
#coding=utf-8

import os

#Debugging
DEBUG=0

#Site information
NAME='msw'
DESCRIPTION='名师网'

# Accounts
ADMIN_USERNAME='admin'
ADMIN_PASSWORD='admin2013$'

# Paths
ROOT_DIR=os.getcwd() 
DATA_DIR=os.path.join(ROOT_DIR, 'data')
TMPL_DIR=os.path.join(ROOT_DIR, 'templates')
STATIC_DIR = os.path.join(ROOT_DIR, 'static')
UPLOAD_DIR = os.path.join(STATIC_DIR, 'uploads')

# URLs
WEB_URL = 'http://msw.wiaapp.cn'
UPLOAD_URL = '/static/uploads'

# Configuration Maximum
MAX_UPLOAD_FILE_SIZE=4*1024*1024
COUNT_PER_PAGE=10

# Database
DATABASE='%s/msw.db' % DATA_DIR if not os.getenv('MSW_DATABASE') else os.getenv('MSW_DATABASE')

# Alipay
ALIPAY_PARTNER="2088911572865213"
ALIPAY_KEY="85af666pw9g56e8lvabro5v430wrr5pv"
ALIPAY_SELLER_EMAIL="3128658714@qq.com"
ALIPAY_MOBILE_PUBLIC_KEY='%s/ali_mobile_public_key.pem' % ROOT_DIR
ALIPAY_MOBILE_PRIVATE_KEY='%s/private_key.pem' % ROOT_DIR
ALIPAY_CACERT='%s/ali_cacert.pem' % ROOT_DIR

# Imaging 
THUMBNAIL_XRES = 112
THUMBNAIL_YRES = 70
THUMBNAIL_QUALITY = 90
THUMBNAIL_DPI = (120, 120)

IMAGE_XRES = 480
IMAGE_YRES = 300
IMAGE_QUALITY = 80
IMAGE_DPI = (100, 100)

# Apps
leancloud_app_id =  '6exxgnzeikhgft4237hyf07e59br0us0xilfojk340bd0hwm'
leancloud_app_key = '4zxt9u6igz4s0vodddk19i0uudxgnhsese2l52449chcm6x4'
leancloud_master_key = '8o4143izsdspjsxy2tko0nvdsxuuvyinmpugx0z74gpl1s4n'

aodianyun_access_id = '260761612629'
aodianyun_access_key = '2p17nX53T6jy325Q657o5lEtIP5s0J5t'
