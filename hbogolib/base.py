# encoding: utf-8
# base add-on class for hbogo Kodi add-on
# Copyright (C) 2019 ArvVoid (https://github.com/arvvoid)
# Relesed under GPL version 2
#########################################################

import urllib

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

    countries = {
        "ba": ['Bosnia and Herzegovina', 'ba', 'ba', 'BIH', 'HRV', '', HANDLER_EU],
        "bg": ['Bulgaria', 'bg', 'bg', 'BGR', 'BUL', '', HANDLER_EU],
        "hr": ['Croatia', 'hr', 'hr', 'HRV', 'HRV', '', HANDLER_EU],
        "cz": ['Czech Republic', 'cz', 'cz', 'CZE', 'CES', '', HANDLER_EU],
        "hu": ['Hungary', 'hu', 'hu', 'HUN', 'HUN', '', HANDLER_EU],
        "mk": ['Macedonia', 'mk', 'mk', 'MKD', 'MKD', '', HANDLER_EU],
        "me": ['Montenegro', 'me', 'me', 'MNE', 'SRP', '', HANDLER_EU],
        "pl": ['Polonia', 'pl', 'pl', 'POL', 'POL', '', HANDLER_EU],
        "pt": ['Portugal', 'pt', 'pt', 'PRT', 'POR', 'https://hboportugal.com', HANDLER_EU],
        "ro": ['Romania', 'ro', 'ro', 'ROU', 'RON', '', HANDLER_EU],
        "rs": ['Serbia', 'rs', 'sr', 'SRB', 'SRP', '', HANDLER_EU],
        "sk": ['Slovakia', 'sk', 'sk', 'SVK', 'SLO', '', HANDLER_EU],
        "si": ['Slovenija', 'si', 'si', 'SVN', 'SLV', '', HANDLER_EU],
    }

    def __init__(self, addon_id, handle, base_url):
        self.base_url = base_url
        self.handle = handle
        self.addon_id = addon_id
        self.addon = xbmcaddon.Addon(self.addon_id)
        self.language = self.addon.getLocalizedString

        country_id = self.addon.getSetting('country_code')

        if country_id not in self.countries:
            self.setup()
        else:
            self.start(country_id)

    def start(self, country_id):
        if self.countries[country_id][6] == self.HANDLER_EU:
            self.handler = HbogoHandler_eu(self.addon_id, self.handle, self.base_url, self.countries[country_id])
        else:
            xbmcgui.Dialog().ok("ERROR", "Unsupported region")
            sys.exit()


    def setup(self):
        # STEP 1, show country selection dialog

        list = []

        for c in self.countries:
            list.append(xbmcgui.ListItem(label=self.countries[c][0], label2=self.countries[c][2], iconImage="https://www.countryflags.io/" + self.countries[c][2] + "/flat/64.png"))

        index = xbmcgui.Dialog().select("Please your country", list, useDetails=True)
        if index != -1:
            country_id = list[index].getLabel2()
            self.addon.setSetting('country_code', country_id)
            self.start(country_id)
        else:
            sys.exit()

    def router(self, arguments):
        params = dict(parse.parse_qsl(arguments))

        url = None
        name = None
        thumbnail = None
        cid = None
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

        elif mode == 6: #logout, destry setup
            self.handler.del_setup()

        elif mode == 7: #reset session
            self.handler.del_login()




