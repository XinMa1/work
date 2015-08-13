# -*- coding: utf-8 -*-
#coding=utf-8

def uuidgen():
    import uuid
    return str(uuid.uuid4())

def hashgen(s):
    import hashlib
    return hashlib.sha224(s).hexdigest()
