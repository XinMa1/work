# -*- coding: utf-8 -*-
#coding=utf-8

import os
import config

class httpUploadedFile(object):
    def __init__(self, rawdata):
        uploadDir = config.UPLOAD_DIR
        uploadTemp = os.path.join(uploadDir, 'temp')

        self._mimetype = None

        from utils import uuidgen
        self._uuid = uuidgen()
        source = os.path.join(uploadTemp, self._uuid)

        open(source, 'w').write(rawdata)

        import magic
        try:
            ms = magic.open(magic.MAGIC_MIME)
            ms.load()
            self._mimetype = ms.file(source).lower().split(';')[0]
            ms.close()
        except Exception, e:
            self._mimetype = magic.from_file(source, mime=True)

        if self._mimetype not in ['application/zip','audio/mpeg', 'image/jpeg','video/mp4']:
            os.unlink(source)
            raise BadFormatError('mimetype not supported!')

        # workaround against mp3 suffix
        if self._mimetype == 'audio/mpeg':
            self._mimetype = 'audio/mp3'

        typeDir = os.path.join(uploadDir, self._mimetype.split('/')[0])
        self._filename = '%s.%s' % (self._uuid, self._mimetype.split('/')[1])
        self._target = os.path.join(typeDir, self._filename)        
        os.rename(source, self._target)
        

    def uuid(self):
        return self._uuid

    def filename(self):
        return self._filename

    def target(self):
        return self._target

    def mimetype(self):
        return self._mimetype

class httpFileSystem(object):
    def __init__(self):
        self.uploadDir = config.UPLOAD_DIR
        self.tempDir = os.path.join(self.uploadDir, 'temp')
        self.videoDir = os.path.join(self.uploadDir, 'video')
        self.audioDir = os.path.join(self.uploadDir, 'audio')
        self.imageDir = os.path.join(self.uploadDir, 'image')

    def audioURIFromUUID(self, uuid):
        return os.path.join(self.audioDir, '%s.mp3' % uuid)

    def videoURIFromUUID(self, uuid):
        return os.path.join(self.videoDir, '%s.mp4' % uuid)

    def imageURIFromUUID(self, uuid):
        return os.path.join(self.imageDir, '%s.jpeg' % uuid)
