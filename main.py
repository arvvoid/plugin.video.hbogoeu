# encoding: utf-8
# base handler class for hbogo Kodi add-on
# Copyright (C) 2019 ArvVoid (https://github.com/arvvoid)
# Relesed under GPL version 2
#########################################################

from hbogolib.base import hbogo
import sys
import xbmc


# Setup plugin
PLUGIN_HANDLE = int(sys.argv[1])
BASE_URL = sys.argv[0]
# We use string slicing to trim the leading ? from the plugin call paramstring
REQUEST_PARAMS = sys.argv[2][1:]


if __name__ == '__main__':
    id = "plugin.video.hbogoeu"
    version = "2.0.5~beta18"
    xbmc.log("[" + id + "]  STARING VERSION: " + version, xbmc.LOGDEBUG)
    addon_main = hbogo(id, PLUGIN_HANDLE, BASE_URL)
    addon_main.router(REQUEST_PARAMS)

