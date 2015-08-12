# -*- coding: utf-8 -*-
#coding=utf-8

import os
import StringIO
import config
from log import log

try:
    import Image 
except:
    log.warn('Python module phthon-imaging is missing!')
    raise 'python-imaging'

'''
Image helper requires to install python-imaging using yum,
or install PIL for other platforms.

See http://www.pythonware.com/products/pil/
''' 
class imaging(object):
    def __init__(self, src):
        self.src = src
        self.im = Image.open(self.src)
        
    def format(self):
        return self.im.format.lower()

    def size(self):
        return self.im.size

    def resize(self, xres, yres, quality=config.IMAGE_QUALITY, dpi=config.IMAGE_DPI, format='JPEG'):
        img = self.im 
        # To workaround issue against cannot write mode P as JPEG      
        if img.mode != 'RGB':
            img = img.convert('RGB')

        resized = img.resize((xres, yres), Image.ANTIALIAS)
        output = StringIO.StringIO()
        resized.save(output, format, dpi=dpi, quality=quality)
        return output.getvalue()

    def thumbnail(self, 
                  xres=config.THUMBNAIL_XRES, 
                  yres=config.THUMBNAIL_YRES, 
                  quality=config.IMAGE_QUALITY, 
                  dpi=config.IMAGE_DPI, format='JPEG'):
        img = self.im
        # To workaround issue against cannot write mode P as JPEG      
        if img.mode != 'RGB':
            img = img.convert('RGB')

        img.thumbnail((xres, yres), Image.ANTIALIAS)
        output = StringIO.StringIO()
        img.save(output, format, dpi=dpi, quality=quality)
        return output.getvalue()

    @staticmethod
    def default_thumbnail():
        default = os.path.join(config.ROOT_DIR, 'static/images/default.jpeg')
        im = imaging(default)
        return im.resize(config.THUMBNAIL_XRES,
                        config.THUMBNAIL_YRES,
                        config.THUMBNAIL_QUALITY,
                        config.THUMBNAIL_DPI)

    @staticmethod
    def system_thumbnail(key):
        f = os.path.join(config.ROOT_DIR, 'static/images/%s.jpeg' % key)
        if not os.path.exists(f):
            return None

        im = imaging(f)
        return im.resize(config.THUMBNAIL_XRES,
                        config.THUMBNAIL_YRES,
                        config.THUMBNAIL_QUALITY,
                        config.THUMBNAIL_DPI)


if __name__ == '__main__':
    example = 'static/photoswipe/examples/images/full/001.jpg'
    buf = open(os.path.join(config.ROOT_DIR, example)).read()
    im = imaging(StringIO.StringIO(buf))
    print im.size()
    open('/tmp/out.jpeg', 'w').write(im.resize(80, 60))
