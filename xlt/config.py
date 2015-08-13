#!/usr/bin/env python
#coding=utf-8

import os

#Debugging
DEBUG=0

#Site information
NAME='xlt'
DESCRIPTION='线缆通'

# Accounts
ADMIN_USERNAME='admin'
ADMIN_PASSWORD='admin2013$'

# Paths
ROOT_DIR = os.getcwd() 
DATA_DIR = os.path.join(ROOT_DIR, 'data')
TMPL_DIR = os.path.join(ROOT_DIR, 'templates')
ADMIN_TMPLS_DIR = os.path.join(TMPL_DIR, 'admin')
WAP_TMPLS_DIR = os.path.join(TMPL_DIR, 'wap')
STATIC_DIR = os.path.join(ROOT_DIR, 'static')
UPLOAD_DIR = os.path.join(STATIC_DIR, 'uploads')

# URLs
WEB_URL = 'http://msw.wiaapp.cn'
UPLOAD_URL = '/static/uploads'

# Configuration Maximum
MAX_UPLOAD_FILE_SIZE=8*1024*1024
COUNT_PER_PAGE=10

# Database
DATABASE='%s/xlt.db' % DATA_DIR if not os.getenv('XLT_DATABASE') else os.getenv('MSW_DATABASE')

# Imaging 
THUMBNAIL_XRES = 112
THUMBNAIL_YRES = 70
THUMBNAIL_QUALITY = 90
THUMBNAIL_DPI = (120, 120)

IMAGE_XRES = 480
IMAGE_YRES = 300
IMAGE_QUALITY = 80
IMAGE_DPI = (100, 100)



