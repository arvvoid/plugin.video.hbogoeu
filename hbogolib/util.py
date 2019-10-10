# encoding: utf-8
# util class for Hbo Go Kodi add-on
# Copyright (C) 2019 ArvVoid (https://github.com/arvvoid)
# Relesed under GPL version 2
#########################################################

from __future__ import absolute_import, division

import sys
import base64
import hashlib

class Util(object):

    @staticmethod
    def base64enc_bytes(data):
        if sys.version_info < (3, 0):
            return base64.b64encode(data)
        else:
            return base64.b64encode(bytes(data, 'utf8'))

    @staticmethod
    def base64enc_string(data):
        if sys.version_info < (3, 0):
            return base64.b64encode(data)
        else:
            return base64.b64encode(bytes(data, 'utf8')).decode('utf8')

    @staticmethod
    def base64dec_string(base64data):
        if sys.version_info < (3, 0):
            return base64.b64decode(base64data)
        else:
            return base64.b64decode(base64data).decode('utf8')

    @staticmethod
    def base64dec_bytes(base64data):
        return base64.b64decode(base64data)

    @staticmethod
    def hash225_bytes(data):
        if sys.version_info < (3, 0):
            return hashlib.sha256(bytes(data)).digest()
        else:
            return hashlib.sha256(bytes(data, 'utf8')).digest()

    @staticmethod
    def hash225_string(data):
        if sys.version_info < (3, 0):
            return hashlib.sha256(bytes(data)).hexdigest()
        else:
            return hashlib.sha256(bytes(data, 'utf8')).hexdigest()
