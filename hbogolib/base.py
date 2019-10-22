# encoding: utf-8
# base class for Hbo Go Kodi add-on
# Copyright (C) 2019 ArvVoid (https://github.com/arvvoid)
# Relesed under GPL version 2
#########################################################

from __future__ import absolute_import, division


from hbogolib.constants import HbogoConstants

try:
    from urllib import unquote_plus as unquote
except ImportError:
    from urllib.parse import unquote_plus as unquote

try:
    import urlparse as parse
except ImportError:
    import urllib.parse as parse

import sys
from kodi_six import xbmc, xbmcaddon, xbmcgui

import traceback


class hbogo(object):

    def __init__(self, handle, base_url):
        self.base_url = base_url
        self.handle = handle
        self.addon = xbmcaddon.Addon()
        self.addon_id = self.addon.getAddonInfo('id')
        self.language = self.addon.getLocalizedString
        self.handler = None

    @staticmethod
    def country_index(country_id):
        index = -1

        for i in range(len(HbogoConstants.countries)):
            if HbogoConstants.countries[i][1] == country_id:
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

        if HbogoConstants.countries[country_index][6] == HbogoConstants.HANDLER_EU:
            from hbogolib.handlereu import HbogoHandler_eu
            self.handler = HbogoHandler_eu(self.handle, self.base_url, HbogoConstants.countries[country_index])
        elif HbogoConstants.countries[country_index][6] == HbogoConstants.HANDLER_SPAIN:
            from hbogolib.handlersp import HbogoHandler_sp
            self.handler = HbogoHandler_sp(self.handle, self.base_url, HbogoConstants.countries[country_index])
        else:
            xbmcgui.Dialog().ok("ERROR", "Unsupported region")
            sys.exit()


    def setup(self):
        # STEP 0 - SETUP DRM
        from inputstreamhelper import Helper
        is_helper = Helper('mpd', drm='com.widevine.alpha')
        is_helper.check_inputstream()

        # STEP 1, show country selection dialog

        li_items_list = []

        for country in HbogoConstants.countries:
            li_items_list.append(xbmcgui.ListItem(label=country[0], label2=country[1]))
            li_items_list[-1].setArt({'thumb': "https://www.countryflags.io/" + country[1] + "/flat/64.png", 'icon': "https://www.countryflags.io/" + country[1] + "/flat/64.png"})
        index = xbmcgui.Dialog().select(self.language(30441).encode('utf-8'), li_items_list, useDetails=True)
        if index != -1:
            country_id = li_items_list[index].getLabel2()
            self.addon.setSetting('country_code', country_id)
        else:
            sys.exit()

    def router(self, arguments):
        params = dict(parse.parse_qsl(arguments))

        url = None
        name = None
        content_id = None
        mode = None
        vote = None


        try:
            url = unquote(params["url"])
        except KeyError:
            pass
        except Exception:
            xbmc.log("[" + str(self.addon_id) + "] " + "ROUTER - url warning: " + traceback.format_exc(), xbmc.LOGDEBUG)
        try:
            name = unquote(params["name"])
        except KeyError:
            pass
        except Exception:
            xbmc.log("[" + str(self.addon_id) + "] " + "ROUTER - name warning: " + traceback.format_exc(), xbmc.LOGDEBUG)
        try:
            mode = int(params["mode"])
        except KeyError:
            pass
        except Exception:
            xbmc.log("[" + str(self.addon_id) + "] " +"ROUTER - mode warning: " + traceback.format_exc(), xbmc.LOGDEBUG)
        try:
            content_id = str(params["cid"])
        except KeyError:
            pass
        except Exception:
            xbmc.log("[" + str(self.addon_id) + "] " +"ROUTER - content_id warning: " + traceback.format_exc(), xbmc.LOGDEBUG)
        try:
            vote = str(params["vote"])
        except KeyError:
            pass
        except Exception:
            xbmc.log("[" + str(self.addon_id) + "] " + "ROUTER - vote warning: " + traceback.format_exc(), xbmc.LOGDEBUG)

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
            self.handler.setDispCat(self.language(30711).encode('utf-8'))
            self.handler.search()

        elif mode == 5:
            self.start()
            self.handler.setDispCat(name)
            self.handler.play(url, content_id)

        elif mode == 6: #logout, destry setup
            #ask confirm
            if xbmcgui.Dialog().yesno(self.addon.getAddonInfo('name'), self.language(30692).encode('utf-8')):
                from hbogolib.handler import HbogoHandler
                handler = HbogoHandler(self.handle, self.base_url)
                handler.del_setup()
                xbmc.executebuiltin('Container.Refresh')

        elif mode == 7: #reset session
            from hbogolib.handler import HbogoHandler
            handler = HbogoHandler(self.handle, self.base_url)
            handler.del_login()
            xbmc.executebuiltin('Container.Refresh')

        elif mode == 8: # vote
            self.start()
            self.handler.procContext(8, content_id, vote)

        elif mode == 9: # add to my list
            self.start()
            self.handler.procContext(9, content_id)

        elif mode == 10: # remove from my list
            self.start()
            self.handler.procContext(10, content_id)




