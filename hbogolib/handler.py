# encoding: utf-8
# generic handler class for hbogo Kodi add-on
# Copyright (C) 2019 ArvVoid (https://github.com/arvvoid)
# Relesed under GPL version 2
#########################################################
# GENERIC HBOGO HANDLER CLASS
#########################################################

import sys
import pickle
import urllib
import os

import requests

import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

class HbogoHandler(object):

    UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    GO_SW_VERSION = '4.7.4'
    GO_REQUIRED_PLATFORM = 'CHBR'  # emulate chrome
    ACCEPT_LANGUAGE = 'en-us,en;q=0.8'

    def __init__(self, addon_id, handle, base_url):
        self.addon_id = addon_id
        self.addon = xbmcaddon.Addon(addon_id)
        self.language = self.addon.getLocalizedString
        self.base_url = base_url
        self.handle = handle
        self.DEBUG_ID_STRING = "[" + str(self.addon_id) + "] "
        self.SESSION_VALIDITY = int(self.addon.getSetting('sessionvalid'))  # stored session valid

        self.base_addon_cat=""

        self.md = xbmc.translatePath(self.addon.getAddonInfo('path') + "/resources/media/")
        self.resources = xbmc.translatePath(self.addon.getAddonInfo('path') + "/resources/")
        self.search_string = urllib.unquote_plus(self.addon.getSetting('lastsearch'))
        xbmcplugin.setPluginFanart(self.handle, image=self.resources + "fanart.jpg")

        # LABELS

        self.LB_SEARCH_DESC = self.language(33700).encode('utf-8')
        self.LB_SEARCH_NORES = self.language(33701).encode('utf-8')
        self.LB_ERROR = self.language(33702).encode('utf-8')
        self.LB_INFO = self.language(33713).encode('utf-8')
        self.LB_EPISODE_UNTILL = self.language(33703).encode('utf-8')
        self.LB_FILM_UNTILL = self.language(33704).encode('utf-8')
        self.LB_EPISODE = self.language(33705).encode('utf-8')
        self.LB_SEASON = self.language(33706).encode('utf-8')
        self.LB_MYPLAYLIST = self.language(33707).encode('utf-8')
        self.LB_NOLOGIN = self.language(33708).encode('utf-8')
        self.LB_LOGIN_ERROR = self.language(33709).encode('utf-8')
        self.LB_NO_OPERATOR = self.language(33710).encode('utf-8')
        self.LB_SEARCH = self.language(33711).encode('utf-8')

        self.use_content_type = "episodes"

        self.force_original_names = self.addon.getSetting('origtitles')
        if self.force_original_names == "true":
            self.force_original_names = True
        else:
            self.force_original_names = False

        self.force_scraper_names = self.addon.getSetting('forcescrap')
        if self.force_scraper_names == "true":
            self.force_scraper_names = True
        else:
            self.force_scraper_names = False

        self.sensitive_debug = self.addon.getSetting('sensitivedebug')
        if self.sensitive_debug == "true":
            self.sensitive_debug = True
        else:
            self.sensitive_debug = False

        if self.sensitive_debug:
            ret = xbmcgui.Dialog().yesno(self.LB_INFO, self.language(33712).encode('utf-8'), self.language(33714).encode('utf-8'), self.language(33715).encode('utf-8'))
            if not ret:
                sys.exit()

        self.loggedin_headers = None  #DEFINE IN SPECIFIC HANDLER
        self.API_PLATFORM = 'COMP'

    def log(self, msg, level=xbmc.LOGDEBUG):
        xbmc.log(self.DEBUG_ID_STRING + msg, level)


    def setDispCat(self, cur_loc):
        xbmcplugin.setPluginCategory(self.handle, cur_loc)

    def send_login_hbogo(self, url, headers, data):
        try:
            r = requests.post(url, headers=headers, data=data)
            return r.json()
        except:
            self.log("SEND LOGIN ERROR")
            resp = {"Data": {"ErrorMessage": "SEND LOGIN ERROR"}, "ErrorMessage": "SEND LOGIN ERROR"}
            return resp

    def get_from_hbogo(self, url):
        try:
            r = requests.get(url, headers=self.loggedin_headers)
            return r.json()
        except:
            self.log("GET FROM HBO ERROR")
            resp = {"Data": {"ErrorMessage": "GET FROM HBO ERROR"}, "ErrorMessage": "GET FROM HBO ERROR"}
            return resp

    def send_purchase_hbogo(self, url, purchase_payload, purchase_headers):
        try:
            r = requests.post(url, headers=purchase_headers, data=purchase_payload)
            return r.json()
        except:
            self.log("SEND HBO PURCHASE ERROR")
            resp = {"Data": {"ErrorMessage": "SEND HBO PURCHASE ERROR"}, "ErrorMessage": "SEND HBO PURCHASE ERROR"}
            return resp

    def del_login(self):
        try:
            folder = xbmc.translatePath("special://temp")
            self.log("Removing stored session: " + folder + self.addon_id + "_session"+".pkl")
            os.remove(folder + self.addon_id + "_session"+".pkl")
        except:
            pass

    def del_setup(self):
        self.del_login()
        self.addon.setSetting('country_code', '')
        self.addon.setSetting('operator_id', '')
        self.addon.setSetting('operator_name', '')
        self.addon.setSetting('operator_is_web', 'true')
        self.addon.setSetting('operator_redirect_url', '')
        self.addon.setSetting('individualization', '')
        self.addon.setSetting('customerId', '')
        self.addon.setSetting('FavoritesGroupId', '')
        self.log("Removed stored setup")

    def save_obj(self, obj, name):
        folder = xbmc.translatePath("special://temp")
        self.log("Saving: " + folder + name + '.pkl')
        with open(folder + name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    def load_obj(self, name):
        folder = xbmc.translatePath("special://temp")
        self.log("Trying to load: " + folder + name + '.pkl')
        try:
            with open(folder + name + '.pkl', 'rb') as f:
                return pickle.load(f)
        except:
            self.log("OBJECT RELOAD ERROR")
            return None

    #IMPLEMENT THESE IN SPECIFIC REGIONAL HANDLER

    def storeIndiv(self, indiv, custid):
        pass

    def storeFavgroup(self, favgroupid):
        pass

    def silentRegister(self):
        pass

    def getFavoriteGroup(self):
        pass

    def setup(self):
        pass

    def logout(self):
        pass

    def login(self):
        pass

    def categories(self):
        pass

    def list(self, url):
        pass

    def season(self, url):
        pass

    def episode(self, url):
        pass

    def search(self):
        pass

    def play(self, url, cid):
        pass

    def addLink(self, title, mode):
        pass

    def addDir(self, item, mode, media_type):
        pass

    def addCat(self, name, url, icon, mode):
        pass


