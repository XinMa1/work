#!/usr/bin/env python
#coding=utf-8

import os

#Debugging
DEBUG=0

#Site information
NAME='PhoneCMS2015'
DESCRIPTION='PhoneCMS 2015'

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
WEB_URL = 'http://demo.wiaapp.cn'
UPLOAD_URL = '/static/uploads'

# Configuration Maximum
MAX_UPLOAD_FILE_SIZE=4*1024*1024
COUNT_PER_PAGE=10

# Database
DATABASE='%s/scg.db' % DATA_DIR if not os.getenv('MSW_DATABASE') else os.getenv('MSW_DATABASE')

# Alipay
ALIPAY_PARTNER="2088711975367873"
ALIPAY_KEY="pj1kvylpm8sd5cccwkuj1hp4q435jyu2"
ALIPAY_SELLER_EMAIL="wx@whhe.cn"
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
leancloud_app_id =  'xbw3h6fvyi0nzu9v6dwl676p6vmxkg0qiz4p92z8h7wgdxq9'
leancloud_app_key = '4cd158x8yrflmghm0ooz675fohwbzbiesxefvyfpsownjk8s'
leancloud_master_key = 'ibuynot7dxcdckeoa394v4y09j2is9dend6puz6rvqsl9rlu'

aodianyun_access_id = '260761612629'
aodianyun_access_key = '2p17nX53T6jy325Q657o5lEtIP5s0J5t'
