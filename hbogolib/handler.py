# encoding: utf-8
# generic handler class for Hbo Go Kodi add-on
# Copyright (C) 2019 ArvVoid (https://github.com/arvvoid)
# Relesed under GPL version 2
#########################################################
# GENERIC HBOGO HANDLER CLASS
#########################################################

from __future__ import absolute_import, division, unicode_literals

import sys
import json
import os
import traceback

import requests

from kodi_six import xbmc, xbmcaddon, xbmcplugin, xbmcgui
from kodi_six.utils import py2_encode, py2_decode

import base64
import codecs
import hashlib
import defusedxml.ElementTree as ET

try:
    import urllib.unquote_plus as unquote
except ImportError:
    from urllib.parse import unquote_plus as unquote

try:
    from Cryptodome import Random
    from Cryptodome.Cipher import AES
    from Cryptodome.Util import Padding
except ImportError:
    # no Cryptodome gracefully fail with an informative message
    msg = xbmcaddon.Addon().getLocalizedString(30694)
    xbmc.log("[" + str(xbmcaddon.Addon().getAddonInfo('id')) + "] MISSING Cryptodome dependency...exiting..." + traceback.format_exc(), xbmc.LOGDEBUG)
    xbmcgui.Dialog().ok(xbmcaddon.Addon().getAddonInfo('name') + " ERROR", msg)
    sys.exit()

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
        self.SESSION_VALIDITY = 0.5  # stored session valid for half hour

        self.base_addon_cat = ""
        self.cur_loc = ""

        self.search_string = unquote(self.addon.getSetting('lastsearch'))
        xbmcplugin.setPluginFanart(self.handle, image=self.get_resource("fanart.jpg"))

        # LABELS

        self.LB_SEARCH_DESC = py2_encode(self.language)
        self.LB_SEARCH_NORES = py2_encode(self.language(30701))
        self.LB_ERROR = py2_encode(self.language(30702))
        self.LB_INFO = py2_encode(self.language(30713))
        self.LB_SUCESS = py2_encode(self.language(30727))
        self.LB_EPISODE_UNTILL = py2_encode(self.language(30703))
        self.LB_FILM_UNTILL = py2_encode(self.language(30704))
        self.LB_EPISODE = py2_encode(self.language(30705))
        self.LB_SEASON = py2_encode(self.language(30706))
        self.LB_MYPLAYLIST = py2_encode(self.language(30707))
        self.LB_NOLOGIN = py2_encode(self.language(30708))
        self.LB_LOGIN_ERROR = py2_encode(self.language(30709))
        self.LB_NO_OPERATOR = self.language(30710).encode('utf-8')
        self.LB_SEARCH = py2_encode(self.language(30711))

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

        self.lograwdata = self.addon.getSetting('lograwdata')
        if self.lograwdata == "true":
            self.lograwdata = True
        else:
            self.lograwdata = False


        if self.sensitive_debug:
            ret = xbmcgui.Dialog().yesno(self.LB_INFO, self.language(30712), self.language(30714), self.language(30715))
            if not ret:
                sys.exit()

        self.loggedin_headers = None  #DEFINE IN SPECIFIC HANDLER
        self.API_PLATFORM = 'COMP'

    @staticmethod
    def get_resource(file):
        return py2_decode(xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')+'/resources/'+file))

    @staticmethod
    def get_media_resource(file):
        return py2_decode(xbmc.translatePath(xbmcaddon.Addon().getAddonInfo('path')+'/resources/media/'+file))

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
                self.log("SEND LOGIN RETURNED RAW: " + py2_encode(r.text))
            if response_format == 'json':
                return r.json()
            elif response_format == 'xml':
                return ET.fromstring(py2_encode(r.text))
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
                return ET.fromstring(py2_encode(r.text))
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
                return ET.fromstring(py2_encode(r.text))
        except requests.RequestException as e:
            self.log("SEND PURCHASE ERROR: " + repr(e))
            resp = {"Data": {"ErrorMessage": "SEND HBO PURCHASE ERROR"}, "ErrorMessage": "SEND HBO PURCHASE ERROR"}
            return resp

    def del_login(self):
        try:
            folder = xbmc.translatePath(self.addon.getAddonInfo('profile'))
            self.log("Removing stored session: " + folder + self.addon_id + "_session"+".pkl")
            os.remove(folder + self.addon_id + "_session"+".pkl")
        except Exception:
            self.log("Delete login error: " + traceback.format_exc())

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
        self.log("Saving: " + folder + name + '.ecdata')
        with open(folder + name + '.ecdata', 'wb') as f:
            f.write(self.encrypt_credential_v1(json.dumps(obj)))

    def load_obj(self, name):
        folder = xbmc.translatePath(self.addon.getAddonInfo('profile'))
        self.log("Trying to load: " + folder + name + '.ecdata')
        try:
            with open(folder + name + '.ecdata', 'rb') as f:
                return json.loads(self.decrypt_credential_v1(f.read()))
        except Exception:
            self.log("OBJECT RELOAD ERROR")
            self.log("Stack trace: " + traceback.format_exc())
            return None

    def inputCredentials(self):
        username = xbmcgui.Dialog().input(self.language(30442), type=xbmcgui.INPUT_ALPHANUM)
        if len(username) == 0:
            ret = xbmcgui.Dialog().yesno(self.LB_ERROR, self.language(30728))
            if not ret:
                self.addon.setSetting('username', '')
                self.addon.setSetting('password', '')
                return False
            else:
                return self.inputCredentials()
        password = xbmcgui.Dialog().input(self.language(30443), type=xbmcgui.INPUT_ALPHANUM, option=xbmcgui.ALPHANUM_HIDE_INPUT)
        if len(password) == 0:
            ret = xbmcgui.Dialog().yesno(self.LB_ERROR, self.language(30728))
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
            ret = xbmcgui.Dialog().yesno(self.LB_ERROR, self.language(30728))
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
        from .uuid_device import get_crypt_key
        dev_key = get_crypt_key()
        if sys.version_info < (3, 0):
            dev_key2 = bytes(dev_key)
        else:
            dev_key2 = bytes(dev_key, 'ascii')
        return hashlib.sha256(dev_key + self.addon_id + '.credentials.v1.' + str(codecs.encode(dev_key2, 'rot_13'))).digest()

    def encrypt_credential_v1(self, raw):
        if sys.version_info < (3, 0):
            raw = bytes(raw)
        else:
            raw = bytes(raw, 'utf-8')
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
        except Exception:
            self.log("Decrypt credentials error: " + traceback.format_exc())
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

    def setup(self, country):
        pass

    def logout(self):
        pass

    def login(self):
        return False

    def categories(self):
        pass

    def list(self, url, simple=False):
        pass

    def season(self, url):
        pass

    def episode(self, url):
        pass

    def search(self):
        pass

    def play(self, url, content_id):
        pass

    def procContext(self, action_type, content_id, optional=""):
        pass

    def addLink(self, title, mode):
        pass

    def addDir(self, item, mode, media_type):
        pass

    def addCat(self, name, url, icon, mode):
        pass


