# -*- coding: utf-8 -*-
#coding=utf-8

import os
import logging

LOGFILE = '/dev/null'
LOGFMT = '%(asctime)s.%(msecs)03d [%(process)d] %(levelname)-6s %(message)s'
LOGDATEFMT = '%Y-%m-%d %H:%M:%S'

logging.basicConfig(filename = LOGFILE, \
                    level = logging.DEBUG,  \
                    format = LOGFMT, \
                    datefmt = LOGDATEFMT)
log = logging.getLogger()


if __name__ == '__main__':
    log.info('this is a info')
    log.debug('this is a debug')
