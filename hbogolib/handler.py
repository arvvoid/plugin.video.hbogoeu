# encoding: utf-8
# generic handler class for Hbo Go Kodi add-on
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

import random
import uuid
import base64
import codecs
import hashlib
import xml.etree.ElementTree as ET
from Cryptodome import Random
from Cryptodome.Cipher import AES
from Cryptodome.Util import Padding
import re




class HbogoHandler(object):

    UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
    GO_SW_VERSION = '4.7.4'
    GO_REQUIRED_PLATFORM = 'CHBR'  # emulate chrome
    ACCEPT_LANGUAGE = 'en-us,en;q=0.8'

    def __init__(self, handle, base_url):
        self.addon = xbmcaddon.Addon()
        self.addon_id = self.addon.getAddonInfo('id')
        self.language = self.addon.getLocalizedString
        self.base_url = base_url
        self.handle = handle
        self.DEBUG_ID_STRING = "[" + str(self.addon_id) + "] "
        self.SESSION_VALIDITY = int(self.addon.getSetting('sessionvalid'))  # stored session valid

        self.base_addon_cat=""
        self.cur_loc = ""

        self.md = xbmc.translatePath(self.addon.getAddonInfo('path') + "/resources/media/")
        self.resources = xbmc.translatePath(self.addon.getAddonInfo('path') + "/resources/")
        self.search_string = urllib.unquote_plus(self.addon.getSetting('lastsearch'))
        xbmcplugin.setPluginFanart(self.handle, image=self.resources + "fanart.jpg")

        # LABELS

        self.LB_SEARCH_DESC = self.language(30700).encode('utf-8')
        self.LB_SEARCH_NORES = self.language(30701).encode('utf-8')
        self.LB_ERROR = self.language(30702).encode('utf-8')
        self.LB_INFO = self.language(30713).encode('utf-8')
        self.LB_SUCESS = self.language(30727).encode('utf-8')
        self.LB_EPISODE_UNTILL = self.language(30703).encode('utf-8')
        self.LB_FILM_UNTILL = self.language(30704).encode('utf-8')
        self.LB_EPISODE = self.language(30705).encode('utf-8')
        self.LB_SEASON = self.language(30706).encode('utf-8')
        self.LB_MYPLAYLIST = self.language(30707).encode('utf-8')
        self.LB_NOLOGIN = self.language(30708).encode('utf-8')
        self.LB_LOGIN_ERROR = self.language(30709).encode('utf-8')
        self.LB_NO_OPERATOR = self.language(30710).encode('utf-8')
        self.LB_SEARCH = self.language(30711).encode('utf-8')

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
            ret = xbmcgui.Dialog().yesno(self.LB_INFO, self.language(30712).encode('utf-8'), self.language(30714).encode('utf-8'), self.language(30715).encode('utf-8'))
            if not ret:
                sys.exit()

        self.loggedin_headers = None  #DEFINE IN SPECIFIC HANDLER
        self.API_PLATFORM = 'COMP'

    def log(self, msg, level=xbmc.LOGDEBUG):
        xbmc.log(self.DEBUG_ID_STRING + msg, level)

    def setDispCat(self, cur_loc):
        xbmcplugin.setPluginCategory(self.handle, cur_loc)
        self.cur_loc = cur_loc

    def send_login_hbogo(self, url, headers, data, response_format='json'):
        self.log("SEND LOGIN URL: " + url)
        self.log("SEND LOGIN RESPONSE FORMAT: " + response_format)
        try:
            r = requests.post(url, headers=headers, data=data)
            self.log("SEND LOGIN RETURNED STATUS: " + str(r.status_code))
            if self.sensitive_debug:
                self.log("SEND LOGIN RETURNED RAW: " + r.text.encode('utf-8'))
            if response_format == 'json':
                return r.json()
            elif response_format == 'xml':
                return ET.fromstring(r.text.encode('utf-8'))
        except requests.RequestException as e:
            self.log("SEND LOGIN ERROR: " + repr(e))
            resp = {"Data": {"ErrorMessage": "SEND LOGIN ERROR"}, "ErrorMessage": "SEND LOGIN ERROR"}
            return resp

    def get_from_hbogo(self, url, response_format='json'):
        self.log("GET FROM HBO URL: " + url)
        self.log("GET FROM HBO RESPONSE FORMAT: " + response_format)
        try:
            r = requests.get(url, headers=self.loggedin_headers)
            self.log("GET FROM HBO STATUS: " + str(r.status_code))
            if response_format == 'json':
                return r.json()
            elif response_format == 'xml':
                return ET.fromstring(r.text.encode('utf-8'))
        except requests.RequestException as e:
            self.log("GET FROM HBO ERROR: " + repr(e))
            resp = {"Data": {"ErrorMessage": "GET FROM HBO ERROR"}, "ErrorMessage": "GET FROM HBO ERROR"}
            return resp

    def send_purchase_hbogo(self, url, purchase_payload, purchase_headers, response_format='json'):
        self.log("SEND PURCHASE URL: " + url)
        self.log("SEND PURCHASE RESPONSE FORMAT: " + response_format)
        try:
            r = requests.post(url, headers=purchase_headers, data=purchase_payload)
            self.log("SEND PURCHASE STATUS: " + str(r.status_code))
            if response_format == 'json':
                return r.json()
            elif response_format == 'xml':
                return ET.fromstring(r.text.encode('utf-8'))
        except requests.RequestException as e:
            self.log("SEND PURCHASE ERROR: " + repr(e))
            resp = {"Data": {"ErrorMessage": "SEND HBO PURCHASE ERROR"}, "ErrorMessage": "SEND HBO PURCHASE ERROR"}
            return resp

    def del_login(self):
        try:
            folder = xbmc.translatePath(self.addon.getAddonInfo('profile'))
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
        self.addon.setSetting('KidsGroupId', '')
        self.addon.setSetting('username', '')
        self.addon.setSetting('password', '')
        self.log("Removed stored setup")

    def save_obj(self, obj, name):
        folder = xbmc.translatePath(self.addon.getAddonInfo('profile'))
        self.log("Saving: " + folder + name + '.pkl')
        with open(folder + name + '.pkl', 'wb') as f:
            pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    def load_obj(self, name):
        folder = xbmc.translatePath(self.addon.getAddonInfo('profile'))
        self.log("Trying to load: " + folder + name + '.pkl')
        try:
            with open(folder + name + '.pkl', 'rb') as f:
                return pickle.load(f)
        except:
            self.log("OBJECT RELOAD ERROR")
            return None

    def inputCredentials(self):
        username = xbmcgui.Dialog().input(self.language(30442).encode('utf-8'), type=xbmcgui.INPUT_ALPHANUM)
        if len(username) == 0:
            ret = xbmcgui.Dialog().yesno(self.LB_ERROR, self.language(30728).encode('utf-8'))
            if not ret:
                self.addon.setSetting('username', '')
                self.addon.setSetting('password', '')
                return False
            else:
                return self.inputCredentials()
        password = xbmcgui.Dialog().input(self.language(30443).encode('utf-8'), type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
        if len(password) == 0:
            ret = xbmcgui.Dialog().yesno(self.LB_ERROR, self.language(30728).encode('utf-8'))
            if not ret:
                self.addon.setSetting('username', '')
                self.addon.setSetting('password', '')
                return False
            else:
                return self.inputCredentials()

        self.setCredential('username', username)
        self.setCredential('password', password)

        self.del_login()
        if self.login():
            return True
        else:
            ret = xbmcgui.Dialog().yesno(self.LB_ERROR, self.language(30728).encode('utf-8'))
            if not ret:
                return False
            else:
                return self.inputCredentials()

    def getCredential(self, credential_id):
        value = self.addon.getSetting(credential_id)
        if value.startswith(self.addon_id + '.credentials.v1.'):
            # this is an encrypted credential
            encoded = value[len(self.addon_id + '.credentials.v1.'):]
            decrypted = self.decrypt_credential_v1(encoded)
            if decrypted is not None:
                return decrypted
            else:
                # decrypt failed ask for credentials again

                if self.inputCredentials():
                    return self.getCredential(credential_id)
                else:
                    return ''
        else:
            # this are old plaintext credentials convert
            if len(value) > 0:
                self.setCredential(credential_id, value)
                return self.getCredential(credential_id)
            else:
                return ''

    def setCredential(self, credential_id, value):
        self.addon.setSetting(credential_id, self.addon_id + '.credentials.v1.' + str(self.encrypt_credential_v1(value)))

    def get_device_id_v1(self):
        space = xbmc.getInfoLabel('System.TotalSpace')
        space = re.sub('[^A-Za-z0-9 ]+', '', space)
        mac = uuid.getnode()
        if (mac >> 40) % 2:
            from platform import node
            mac = node()
        return hashlib.sha256(codecs.encode(str(mac), 'rot_13') + self.addon_id + '.credentials.v1.' + codecs.encode(str(space), 'rot_13')).digest()

    def encrypt_credential_v1(self, raw):
        raw = bytes(Padding.pad(data_to_pad=raw, block_size=32))
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.get_device_id_v1(), AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt_credential_v1(self, enc):
        try:
            enc = base64.b64decode(enc)
            iv = enc[:AES.block_size]
            cipher = AES.new(self.get_device_id_v1(), AES.MODE_CBC, iv)
            decoded = Padding.unpad(padded_data=cipher.decrypt(enc[AES.block_size:]), block_size=32).decode('utf-8')
            return decoded
        except:
            return None

    # IMPLEMENT THESE IN SPECIFIC REGIONAL HANDLER

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
        return False

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

    def procContext(self, type, content_id, optional=""):
        pass

    def addLink(self, title, mode):
        pass

    def addDir(self, item, mode, media_type):
        pass

    def addCat(self, name, url, icon, mode):
        pass


