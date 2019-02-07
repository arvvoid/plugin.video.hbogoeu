# encoding: utf-8
# base handler class for hbogo Kodi add-on
# Copyright (C) 2019 ArvVoid (https://github.com/arvvoid)
# Relesed under GPL version 2
#########################################################

from hbogolib.base import hbogo
import sys


# Setup plugin
PLUGIN_HANDLE = int(sys.argv[1])
BASE_URL = sys.argv[0]
# We use string slicing to trim the leading ? from the plugin call paramstring
REQUEST_PARAMS = sys.argv[2][1:]

if __name__ == '__main__':
    addon_main = hbogo("plugin.video.hbogoeu", PLUGIN_HANDLE, BASE_URL)
    addon_main.router(REQUEST_PARAMS)

