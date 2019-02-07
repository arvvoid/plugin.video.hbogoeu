# encoding: utf-8
# base handler class for hbogo Kodi add-on
# Copyright (C) 2019 ArvVoid (https://github.com/arvvoid)
# Relesed under GPL version 2
#########################################################

from hbogolib.handlereu import HbogoHandler_eu

import urllib
try:
    import urllib.parse as parse
except ImportError:
    import urlparse as parse

import sys
import xbmcaddon
import xbmcgui

class hbogo(object):

    countries = [
        ['N/A', '--', '--', '---', '---'],
        ['Bosnia and Herzegovina', 'ba', 'ba', 'BIH', 'HRV', 'hbogo.eu'],
        ['Bulgaria', 'bg', 'bg', 'BGR', 'BUL', 'hbogo.eu'],
        ['Croatia', 'hr', 'hr', 'HRV', 'HRV', 'hbogo.eu'],
        ['Czech Republic', 'cz', 'cz', 'CZE', 'CES', 'hbogo.eu'],
        ['Hungary', 'hu', 'hu', 'HUN', 'HUN', 'hbogo.eu'],
        ['Macedonia', 'mk', 'mk', 'MKD', 'MKD', 'hbogo.eu'],
        ['Montenegro', 'me', 'me', 'MNE', 'SRP', 'hbogo.eu'],
        ['Polonia', 'pl', 'pl', 'POL', 'POL', 'hbogo.eu'],
        ['Romania', 'ro', 'ro', 'ROU', 'RON', 'hbogo.eu'],
        ['Serbia', 'rs', 'sr', 'SRB', 'SRP', 'hbogo.eu'],
        ['Slovakia', 'sk', 'sk', 'SVK', 'SLO', 'hbogo.eu'],
        ['Slovenija', 'si', 'si', 'SVN', 'SLV', 'hbogo.eu'],
    ]

    def __init__(self, addon_id, handle, base_url):
        self.base_url = base_url
        self.handle = handle
        self.addon_id = addon_id
        self.addon = xbmcaddon.Addon(self.addon_id)
        self.language = self.addon.getLocalizedString
        c_id = int(self.addon.getSetting('country'))

        if c_id==0:
            xbmcgui.Dialog().ok(self.language(33702).encode('utf-8'), self.language(32104).encode('utf-8'))
            xbmcaddon.Addon(id=self.addon_id).openSettings()
            sys.exit()

        try:
            self.country = self.countries[c_id]
        except:
            xbmcgui.Dialog().ok(self.language(33702).encode('utf-8'), self.language(32104).encode('utf-8'))
            xbmcaddon.Addon(id=self.addon_id).openSettings()
            sys.exit()

        if self.country[5] == 'hbogo.eu':
            self.handler=HbogoHandler_eu(self.addon_id, self.handle, self.base_url, self.country)
        else:
            xbmcgui.Dialog().ok("ERROR", "Unsupported region")
            xbmcaddon.Addon(id=self.addon_id).openSettings()
            sys.exit()

    def router(self, arguments):
        params = dict(parse.parse_qsl(arguments))

        url = None
        name = None
        thumbnail = None
        cid = None
        mode = None
        op_id = None
        op_name = None
        is_web = None


        try:
            url = urllib.unquote_plus(params["url"])
        except:
            pass
        try:
            name = urllib.unquote_plus(params["name"])
        except:
            pass
        try:
            thumbnail = str(params["thumbnail"])
        except:
            pass
        try:
            mode = int(params["mode"])
        except:
            pass
        try:
            content_id = str(params["cid"])
        except:
            pass
        try:
            op_id = str(params["op_id"])
        except:
            pass
        try:
            op_name = str(params["op_name"])
        except:
            pass
        try:
            is_web = str(params["is_web"])
        except:
            pass

        if mode == None or url == None or len(url) < 1:
            self.handler.categories()

        elif mode == 1:
            self.handler.setDispCat(name)
            self.handler.list(url)

        elif mode == 2:
            self.handler.setDispCat(name)
            self.handler.season(url)

        elif mode == 3:
            self.handler.setDispCat(name)
            self.handler.episode(url)

        elif mode == 4:
            self.handler.setDispCat(self.language(33711).encode('utf-8'))
            self.handler.search()

        elif mode == 5:
            self.handler.setDispCat(name)
            self.handler.play(url, content_id)

        elif mode == 6:
            self.handler.silentRegister()

        elif mode == 7:
            self.handler.login()

        elif mode == 8:
            self.handler.storeOperator(op_id, is_web, op_name, url)

        elif mode == 9:
            self.handler.logout()

