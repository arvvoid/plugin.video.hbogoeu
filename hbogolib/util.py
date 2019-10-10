# encoding: utf-8
# util class for Hbo Go Kodi add-on
# Copyright (C) 2019 ArvVoid (https://github.com/arvvoid)
# Relesed under GPL version 2
#########################################################

from __future__ import absolute_import, division, unicode_literals

import sys
import base64
import hashlib

class Util(object):

    @staticmethod
    def base64enc(data):
        if sys.version_info < (3, 0):
            return base64.b64encode(bytes(data))
        else:
            return base64.b64encode(bytes(data, 'utf8')).encode('ascii')

    @staticmethod
    def base64dec(base64data):
        if sys.version_info < (3, 0):
            return base64.b64decode(base64data)
        else:
            return base64.b64decode(base64data).encode('utf8')

    @staticmethod
    def hash225_bytes(data):
        if sys.version_info < (3, 0):
            return bytes(hashlib.sha256(bytes(data)).digest())
        else:
            return bytes(hashlib.sha256(bytes(data, 'utf8')).digest())

    @staticmethod
    def hash225(data):
        if sys.version_info < (3, 0):
            return hashlib.sha256(bytes(data)).hexdigest()
        else:
            return hashlib.sha256(bytes(data, 'utf8')).hexdigest()
