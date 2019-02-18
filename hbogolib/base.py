# encoding: utf-8
# base add-on class for hbogo Kodi add-on
# Copyright (C) 2019 ArvVoid (https://github.com/arvvoid)
# Relesed under GPL version 2
#########################################################

import urllib

from hbogolib.handler import HbogoHandler
from hbogolib.handlereu import HbogoHandler_eu

try:
    import urllib.parse as parse
except ImportError:
    import urlparse as parse

import sys
import xbmc
import xbmcaddon
import xbmcgui

class hbogo(object):
    #supported countrys:
    #   0 name
    #   1 national domain
    #   2 country code short
    #   3 country code long
    #   4 default language code
    #   5 special domain
    #   6 hbogo region/handler to use

    HANDLER_EU = 0
    HANDLER_NORDIC = 1
    HANDLER_SPAIN = 1
    HANDLER_US = 2
    HANDLER_LATIN_AMERICA = 3
    HANDLER_ASIA = 4

    countries = [
        ['Bosnia and Herzegovina', 'ba', 'ba', 'BIH', 'HRV', '', HANDLER_EU],
        ['Bulgaria', 'bg', 'bg', 'BGR', 'BUL', '', HANDLER_EU],
        ['Croatia', 'hr', 'hr', 'HRV', 'HRV', '', HANDLER_EU],
        ['Czech Republic', 'cz', 'cz', 'CZE', 'CES', '', HANDLER_EU],
        ['Hungary', 'hu', 'hu', 'HUN', 'HUN', '', HANDLER_EU],
        ['Macedonia', 'mk', 'mk', 'MKD', 'MKD', '', HANDLER_EU],
        ['Montenegro', 'me', 'me', 'MNE', 'SRP', '', HANDLER_EU],
        ['Polonia', 'pl', 'pl', 'POL', 'POL', '', HANDLER_EU],
        ['Portugal', 'pt', 'pt', 'PRT', 'POR', 'https://hboportugal.com', HANDLER_EU],
        ['Romania', 'ro', 'ro', 'ROU', 'RON', '', HANDLER_EU],
        ['Serbia', 'rs', 'sr', 'SRB', 'SRP', '', HANDLER_EU],
        ['Slovakia', 'sk', 'sk', 'SVK', 'SLO', '', HANDLER_EU],
        ['Slovenija', 'si', 'si', 'SVN', 'SLV', '', HANDLER_EU],
    ]

    def __init__(self, addon_id, handle, base_url):
        self.base_url = base_url
        self.handle = handle
        self.addon_id = addon_id
        self.addon = xbmcaddon.Addon(self.addon_id)
        self.language = self.addon.getLocalizedString
        self.handler = None

    def country_index(self, country_id):
        index = -1

        for i in range(len(self.countries)):
            if self.countries[i][2] == country_id:
                index = i
                break

        return index

    def start(self):
        country_id = self.addon.getSetting('country_code')
        country_index = self.country_index(country_id)

        if country_index == -1:
            self.setup()
            country_id = self.addon.getSetting('country_code')
            country_index = self.country_index(country_id)
            if country_index == -1:
                xbmcgui.Dialog().ok("ERROR", "Setup failed")
                sys.exit()

        if self.countries[country_index][6] == self.HANDLER_EU:
            self.handler = HbogoHandler_eu(self.addon_id, self.handle, self.base_url, self.countries[country_index])
        else:
            xbmcgui.Dialog().ok("ERROR", "Unsupported region")
            sys.exit()


    def setup(self):
        # STEP 1, show country selection dialog

        list = []

        for country in self.countries:
            list.append(xbmcgui.ListItem(label=country[0], label2=country[2], iconImage="https://www.countryflags.io/" + country[2] + "/flat/64.png"))

        index = xbmcgui.Dialog().select(self.language(33441), list, useDetails=True)
        if index != -1:
            country_id = list[index].getLabel2()
            self.addon.setSetting('country_code', country_id)
        else:
            sys.exit()

    def router(self, arguments):
        params = dict(parse.parse_qsl(arguments))

        url = None
        name = None
        thumbnail = None
        content_id = None
        mode = None


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

        if mode == None or url == None or len(url) < 1:
            self.start()
            self.handler.categories()

        elif mode == 1:
            self.start()
            self.handler.setDispCat(name)
            self.handler.list(url)

        elif mode == 2:
            self.start()
            self.handler.setDispCat(name)
            self.handler.season(url)

        elif mode == 3:
            self.start()
            self.handler.setDispCat(name)
            self.handler.episode(url)

        elif mode == 4:
            self.start()
            self.handler.setDispCat(self.language(33711).encode('utf-8'))
            self.handler.search()

        elif mode == 5:
            self.start()
            self.handler.setDispCat(name)
            self.handler.play(url, content_id)

        elif mode == 6: #logout, destry setup
            handler = HbogoHandler(self.addon_id, self.handle, self.base_url)
            handler.del_setup()
            xbmc.executebuiltin('Container.Refresh')

        elif mode == 7: #reset session
            handler = HbogoHandler(self.addon_id, self.handle, self.base_url)
            handler.del_login()
            xbmc.executebuiltin('Container.Refresh')




