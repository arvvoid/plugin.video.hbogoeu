# encoding: utf-8
# base handler class for hbogo Kodi add-on
# Copyright (C) 2019 ArvVoid (https://github.com/arvvoid)
# Derived from version v.2.0-beta5 of the add-on, witch was initialy
# derived from https://github.com/billsuxx/plugin.video.hbogohu witch is
# derived from https://kodibg.org/forum/thread-504.html
# Relesed under GPL version 2
#########################################################
# http://hbogo.eu HBOGO HANDLER CLASS
#########################################################


from hbogolib.handler import HbogoHandler

import sys
import os
import time
import urllib
import requests
import json
import base64
import hashlib
import re

import xbmc
import xbmcgui
import xbmcplugin
import inputstreamhelper

class HbogoHandler_eu(HbogoHandler):

    def __init__(self, addon_id, handle, base_url, country):
        HbogoHandler.__init__(self, addon_id, handle, base_url)


        self.COUNTRY_CODE_SHORT = country[2]
        xbmc.log(self.DEBUG_ID_STRING + "OPERATOR COUNTRY_CODE_SHORT: " + self.COUNTRY_CODE_SHORT)
        self.COUNTRY_CODE = country[3]
        xbmc.log(self.DEBUG_ID_STRING + "OPERATOR COUNTRY_CODE: " + self.COUNTRY_CODE)
        self.DEFAULT_LANGUAGE = country[4]
        xbmc.log(self.DEBUG_ID_STRING + "DEFAULT HBO GO LANGUAGE: " + self.DEFAULT_LANGUAGE)
        self.DOMAIN_CODE = country[1]

        #GEN API URLS

        # API URLS
        self.LANGUAGE_CODE = self.DEFAULT_LANGUAGE

        if self.language(32000) == 'ENG':  # only englih or the default language for the selected operator is allowed
            self.LANGUAGE_CODE = 'ENG'

        # check if default language is forced
        if self.addon.getSetting('deflang') == 'true':
            self.LANGUAGE_CODE = self.DEFAULT_LANGUAGE

        self.LICENSE_SERVER = 'https://lic.drmtoday.com/license-proxy-widevine/cenc/'

        self.API_HOST = self.COUNTRY_CODE_SHORT + 'api.hbogo.eu'
        self.API_HOST_REFERER = 'https://hbogo.' + self.DOMAIN_CODE + '/'
        self.base_addon_cat = "hbogo." + self.DOMAIN_CODE + " / "
        self.API_HOST_ORIGIN = 'https://www.hbogo.' + self.DOMAIN_CODE
        self.API_HOST_GATEWAY = 'https://gateway.hbogo.eu'
        self.API_HOST_GATEWAY_REFERER = 'https://gateway.hbogo.eu/signin/form'

        self.API_URL_SILENTREGISTER = 'https://' + self.COUNTRY_CODE_SHORT + '.hbogo.eu/services/settings/silentregister.aspx'

        self.API_URL_SETTINGS = 'https://' + self.API_HOST + '/v7/Settings/json/' + self.LANGUAGE_CODE + '/' + self.API_PLATFORM
        self.API_URL_AUTH_WEBBASIC = 'https://api.ugw.hbogo.eu/v3.0/Authentication/' + self.COUNTRY_CODE + '/JSON/' + self.LANGUAGE_CODE + '/' + self.API_PLATFORM
        self.API_URL_AUTH_OPERATOR = 'https://' + self.COUNTRY_CODE_SHORT + 'gwapi.hbogo.eu/v2.1/Authentication/json/' + self.LANGUAGE_CODE + '/' + self.API_PLATFORM
        self.API_URL_CUSTOMER_GROUP = 'https://' + self.API_HOST + '/v7/CustomerGroup/json/' + self.LANGUAGE_CODE + '/' + self.API_PLATFORM + '/'
        self.API_URL_GROUPS = 'https://' + self.API_HOST + '/v5/Groups/json/' + self.LANGUAGE_CODE + '/' + self.API_PLATFORM
        self.API_URL_CONTENT = 'http://' + self.API_HOST + '/v5/Content/json/' + self.LANGUAGE_CODE + '/' + self.API_PLATFORM + '/'
        self.API_URL_PURCHASE = 'https://' + self.API_HOST + '/v5/Purchase/Json/' + self.LANGUAGE_CODE + '/' + self.API_PLATFORM
        self.API_URL_SEARCH = 'https://' + self.API_HOST + '/v5/Search/Json/' + self.LANGUAGE_CODE + '/' + self.API_PLATFORM + '/'

        self.API_URL_GET_WEB_OPERATORS = 'https://api.ugw.hbogo.eu/v3.0/Operators/' + self.COUNTRY_CODE + '/JSON/' + self.LANGUAGE_CODE + '/' + self.API_PLATFORM
        self.API_URL_GET_OPERATORS = 'https://' + self.COUNTRY_CODE_SHORT + 'gwapi.hbogo.eu/v2.1/Operators/json/' + self.COUNTRY_CODE + '/' + self.API_PLATFORM

        self.individualization = ""
        self.goToken = ""
        self.customerId = ""
        self.GOcustomerId = ""
        self.sessionId = '00000000-0000-0000-0000-000000000000'
        self.FavoritesGroupId = ""

        self.loggedin_headers = {
            'User-Agent': self.UA,
            'Accept': '*/*',
            'Accept-Language': self.ACCEPT_LANGUAGE,
            'Referer': self.API_HOST_REFERER,
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin': self.API_HOST_ORIGIN,
            'X-Requested-With': 'XMLHttpRequest',
            'GO-Language': self.LANGUAGE_CODE,
            'GO-requiredPlatform': self.GO_REQUIRED_PLATFORM,
            'GO-Token': '',
            'GO-SessionId': '',
            'GO-swVersion': self.GO_SW_VERSION,
            'GO-CustomerId': '',
            'Connection': 'keep-alive',
            'Accept-Encoding': ''
        }

    def storeIndiv(self, indiv, custid):
        self.individualization = self.addon.getSetting('individualization')
        if self.individualization == "":
            self.addon.setSetting('individualization', indiv)
            self.addon.individualization = indiv

        self.customerId = self.addon.getSetting('customerId')
        if self.customerId == "":
            self.addon.setSetting('customerId', custid)
            self.customerId = custid

    def storeFavgroup(self, favgroupid):
        self.FavoritesGroupId = self.addon.getSetting('FavoritesGroupId')
        if self.FavoritesGroupId == "":
            self.addon.setSetting('FavoritesGroupId', favgroupid)
            self.FavoritesGroupId = favgroupid

    def silentRegister(self):
        xbmc.log(self.DEBUG_ID_STRING + "DEVICE REGISTRATION")
        jsonrsp = self.get_from_hbogo(self.API_URL_SILENTREGISTER)
        xbmc.log(self.DEBUG_ID_STRING + "DEVICE REGISTRATION: " + str(jsonrsp))
        try:
            if jsonrsp['Data']['ErrorMessage']:
                xbmcgui.Dialog().ok(self.LB_ERROR, jsonrsp['Data']['ErrorMessage'])
                self.logout()
                return
            indiv = jsonrsp['Data']['Customer']['CurrentDevice']['Individualization']
            custid = jsonrsp['Data']['Customer']['CurrentDevice']['Id']
            self.storeIndiv(indiv, custid)

            self.sessionId = jsonrsp['Data']['SessionId']
        except:
            self.logout()
            xbmc.log(self.DEBUG_ID_STRING + "DEVICE REGISTRATION: UNEXPECTED PROBLEM")
            return
        xbmc.log(self.DEBUG_ID_STRING + "DEVICE REGISTRATION: OK")
        return jsonrsp

    def getFavoriteGroup(self):
        jsonrsp = self.get_from_hbogo(self.API_URL_SETTINGS)

        self.favgroupId = jsonrsp['FavoritesGroupId']
        self.storeFavgroup(self.favgroupId)

    def storeOperator(self, op_id, web, name, redirecturl):
        xbmc.log(self.DEBUG_ID_STRING + "Storing operator: " + op_id + ", " + web + ", " + name + ", " + redirecturl)
        self.del_login()
        self.goToken = ""
        self.customerId = ""
        self.GOcustomerId = ""
        self.sessionId = '00000000-0000-0000-0000-000000000000'
        self.loggedin_headers['GO-SessionId'] = str(self.sessionId)
        self.loggedin_headers['GO-Token'] = str(self.goToken)
        self.loggedin_headers['GO-CustomerId'] = str(self.GOcustomerId)

        self.addon.setSetting('OperatorId', op_id)
        self.addon.setSetting('OperatorWeb', web)
        self.addon.setSetting('OperatorName', name)
        if redirecturl!='NOREDIR':
            self.addon.setSetting('OperatorRedirUrl', redirecturl)
        else:
            self.addon.setSetting('OperatorRedirUrl', '')
        self.categories()

    def showOperators(self):
        self.setDispCat(self.language(32102))
        xbmcplugin.addSortMethod(self.handle, xbmcplugin.SORT_METHOD_NONE)
        json_web_operators = requests.get(self.API_URL_GET_WEB_OPERATORS).json()
        xbmc.log(self.DEBUG_ID_STRING + "Get web operators: "+str(json_web_operators))
        cleanr = re.compile('<.*?>')
        for operator in json_web_operators['Items']:
            name = operator['Name']
            liz = xbmcgui.ListItem(name, thumbnailImage=self.resources + "icon.png")
            liz.setInfo(type="Video",
                        infoLabels={"plot": self.language(32100)+" "+self.API_HOST_ORIGIN + os.linesep + os.linesep + self.language(32101)})
            u = self.base_url + "?mode=8&op_id="+operator['Id']+"&op_name="+urllib.quote_plus(name.encode('utf-8', 'ignore'))+"&is_web=true&url=NOREDIR"
            liz.setProperty('isPlayable', "false")
            xbmcplugin.addDirectoryItem(handle=self.handle, url=u, listitem=liz, isFolder=True)
        json_operators = requests.get(self.API_URL_GET_OPERATORS).json()
        xbmc.log(self.DEBUG_ID_STRING + "Get operators" + str(json_operators))
        for operator in json_operators['Items']:
            name = operator['Name']
            desc = re.sub(cleanr, '', operator['Description'])
            redirect = 'NOREDIR'
            if len(operator['RedirectionUrl'])>0:
                redirect=urllib.quote_plus(operator['RedirectionUrl'])
            liz = xbmcgui.ListItem(name, thumbnailImage=operator['LogoUrl'])
            liz.setInfo(type="Video",
                        infoLabels={"plot":  desc + os.linesep + os.linesep + self.language(32101)})
            u = self.base_url + "?mode=8&op_id="+operator['Id']+"&op_name="+urllib.quote_plus(name.encode('utf-8', 'ignore'))+"&is_web=false&url=" + redirect
            liz.setProperty('isPlayable', "false")
            xbmcplugin.addDirectoryItem(handle=self.handle, url=u, listitem=liz, isFolder=False)
        xbmcplugin.endOfDirectory(self.handle)
        xbmcgui.Dialog().ok(self.LB_INFO, self.language(32103))
        sys.exit()

    def chk_login(self):
        return (self.loggedin_headers['GO-SessionId']!='00000000-0000-0000-0000-000000000000' and len(self.loggedin_headers['GO-Token'])!=0 and len(self.loggedin_headers['GO-CustomerId'])!=0)

    def logout(self):
        xbmc.log(self.DEBUG_ID_STRING + "Loging out")
        self.del_login()
        self.goToken = ""
        self.customerId = ""
        self.GOcustomerId = ""
        self.sessionId = '00000000-0000-0000-0000-000000000000'
        self.loggedin_headers['GO-SessionId'] = str(self.sessionId)
        self.loggedin_headers['GO-Token'] = str(self.goToken)
        self.loggedin_headers['GO-CustomerId'] = str(self.GOcustomerId)
        self.showOperators()


    def login(self):
        op_id = self.addon.getSetting('OperatorId')
        if op_id == "":
            xbmc.log(self.DEBUG_ID_STRING + "NO OPERATOR ID: Showing operators selection")
            self.logout()
            return
        xbmc.log(self.DEBUG_ID_STRING + "Using operator: "+str(self.addon.getSetting('OperatorName')))
        xbmc.log(self.DEBUG_ID_STRING + "Using operator: " + str(op_id))

        is_op_web = self.addon.getSetting('OperatorWeb')
        if is_op_web == "true":
            is_op_web = True
        else:
            is_op_web = False
        xbmc.log(self.DEBUG_ID_STRING + "Using operator: IS WEB ? " + str(is_op_web))

        REDIRECT_URL = self.addon.getSetting('OperatorRedirUrl')
        xbmc.log(self.DEBUG_ID_STRING + "Using operator: REDIRECTION URL:  " + str(REDIRECT_URL))

        username = self.addon.getSetting('username')
        password = self.addon.getSetting('password')
        self.customerId = self.addon.getSetting('customerId')
        self.individualization = self.addon.getSetting('individualization')
        self.FavoritesGroupId = self.addon.getSetting('FavoritesGroupId')

        if (self.individualization == "" or self.customerId == ""):
            self.silentRegister()

        if (self.FavoritesGroupId == ""):
            self.getFavoriteGroup()

        if (username == "" or password == ""):
            xbmcgui.Dialog().ok(self.LB_LOGIN_ERROR, self.LB_NOLOGIN)
            self.addon.openSettings()
            sys.exit()
            return

        login_hash = hashlib.sha224(self.individualization + self.customerId + self.FavoritesGroupId + username + password + op_id).hexdigest()
        xbmc.log(self.DEBUG_ID_STRING + "LOGIN HASH: " + login_hash)

        loaded_session = self.load_obj(self.addon_id + "_session")

        if loaded_session != None:
            # sesion exist if valid restore
            xbmc.log(self.DEBUG_ID_STRING + "SAVED SESSION LOADED")
            if loaded_session["hash"] == login_hash:
                xbmc.log(self.DEBUG_ID_STRING + "HASH IS VALID")
                if time.time() < (loaded_session["time"] + (self.SESSION_VALIDITY * 60 * 60)):
                    xbmc.log(self.DEBUG_ID_STRING + "NOT EXPIRED RESTORING...")
                    # valid loaded sesion restor and exit login
                    if self.sensitive_debug:
                        xbmc.log(self.DEBUG_ID_STRING + "Restoring login from saved: " + str(loaded_session))
                    else:
                        xbmc.log(self.DEBUG_ID_STRING + "Restoring login from saved: [OMITTED FOR PRIVACY]")
                    self.loggedin_headers = loaded_session["headers"]
                    self.sessionId = self.loggedin_headers['GO-SessionId']
                    self.goToken = self.loggedin_headers['GO-Token']
                    self.GOcustomerId = self.loggedin_headers['GO-CustomerId']
                    if self.sensitive_debug:
                        xbmc.log(self.DEBUG_ID_STRING + "Login restored - Token" + str(self.goToken))
                        xbmc.log(self.DEBUG_ID_STRING + "Login restored - Customer Id" + str(self.GOcustomerId))
                        xbmc.log(self.DEBUG_ID_STRING + "Login restored - Session Id" + str(self.sessionId))
                    else:
                        xbmc.log(self.DEBUG_ID_STRING + "Login restored - Token  [OMITTED FOR PRIVACY]")
                        xbmc.log(self.DEBUG_ID_STRING + "Login restored - Customer Id  [OMITTED FOR PRIVACY]")
                        xbmc.log(self.DEBUG_ID_STRING + "Login restored - Session Id [OMITTED FOR PRIVACY]")
                    return

        headers = {
            'Origin': self.API_HOST_GATEWAY,
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': self.ACCEPT_LANGUAGE,
            'User-Agent': self.UA,
            'GO-Token': '',
            'Accept': 'application/json',
            'GO-SessionId': '',
            'Referer': self.API_HOST_GATEWAY_REFERER,
            'Connection': 'keep-alive',
            'GO-CustomerId': '00000000-0000-0000-0000-000000000000',
            'Content-Type': 'application/json',
        }

        if is_op_web:
            url = self.API_URL_AUTH_WEBBASIC
        else:
            url = self.API_URL_AUTH_OPERATOR

        if len(REDIRECT_URL) > 0:
            xbmc.log(self.DEBUG_ID_STRING + "OPERATOR WITH LOGIN REDIRECT DETECTED, THE LOGIN WILL PROBABLY FAIL, NOT IMPLEMENTED, more details https://github.com/arvvoid/plugin.video.hbogoeu  ISSUE #5 ")
            # EXPLANATION
            # ------------
            # For a few operators the login is not performed directly using the hbogo api. Instead the user is redirected to the operator website
            # the login is performed there, and then the operator login the user on hbogo and redirect back.
            # What exactly happens and how, will have to be figured out and then implemented in the add-on for those operators to work.
            # For more information go to https://github.com/arvvoid/plugin.video.hbogoeu  ISSUE #5

        data_obj = {
            "Action": "L",
            "AppLanguage": None,
            "ActivationCode": None,
            "AllowedContents": [],
            "AudioLanguage": None,
            "AutoPlayNext": False,
            "BirthYear": 1,
            "CurrentDevice": {
                "AppLanguage": "",
                "AutoPlayNext": False,
                "Brand": "Chromium",
                "CreatedDate": "",
                "DeletedDate": "",
                "Id": "00000000-0000-0000-0000-000000000000",
                "Individualization": self.individualization,
                "IsDeleted": False,
                "LastUsed": "",
                "Modell": "71",
                "Name": "",
                "OSName": "Ubuntu",
                "OSVersion": "undefined",
                "Platform": self.API_PLATFORM,
                "SWVersion": "3.3.9.6418.2100",
                "SubtitleSize": ""
            },
            "CustomerCode": "",
            "DebugMode": False,
            "DefaultSubtitleLanguage": None,
            "EmailAddress": username,
            "FirstName": "",
            "Gender": 0,
            "Id": "00000000-0000-0000-0000-000000000000",
            "IsAnonymus": True,
            "IsPromo": False,
            "Language": self.LANGUAGE_CODE,
            "LastName": "",
            "Nick": "",
            "NotificationChanges": 0,
            "OperatorId": op_id,
            "OperatorName": "",
            "OperatorToken": "",
            "ParentalControl": {
                "Active": False,
                "Password": "",
                "Rating": 0,
                "ReferenceId": "00000000-0000-0000-0000-000000000000"
            },
            "Password": password,
            "PromoCode": "",
            "ReferenceId": "00000000-0000-0000-0000-000000000000",
            "SecondaryEmailAddress": "",
            "SecondarySpecificData": None,
            "ServiceCode": "",
            "SubscribeForNewsletter": False,
            "SubscState": None,
            "SubtitleSize": "",
            "TVPinCode": "",
            "ZipCode": ""
        }

        data = json.dumps(data_obj)
        if self.sensitive_debug:
            xbmc.log(self.DEBUG_ID_STRING + "PERFORMING LOGIN: " + str(data))
        else:
            xbmc.log(self.DEBUG_ID_STRING + "PERFORMING LOGIN")
        jsonrspl = self.send_login_hbogo(url, headers, data)

        try:
            if jsonrspl['ErrorMessage']:
                xbmc.log(self.DEBUG_ID_STRING + "LOGIN ERROR: " + str(jsonrspl['ErrorMessage']))
                xbmcgui.Dialog().ok(self.LB_LOGIN_ERROR, str(jsonrspl['ErrorMessage']))
                if len(REDIRECT_URL) > 0:
                    xbmcgui.Dialog().ok(self.LB_ERROR, "OPERATOR WITH LOGIN REDIRECTION DETECTED. LOGIN REDIRECTION IS NOT CURRENTLY IMPLEMENTED. TO FIND OUT MORE ABOUTE THE ISSUE AND/OR CONTRIBUTE GO TO https://github.com/arvvoid/plugin.video.hbogoeu  ISSUE #5 ")
                self.logout()
                return
        except:
            pass

        try:
            self.customerId = jsonrspl['Customer']['CurrentDevice']['Id']
            self.individualization = jsonrspl['Customer']['CurrentDevice']['Individualization']
        except:
            xbmc.log(self.DEBUG_ID_STRING + "GENERIC LOGIN ERROR")
            xbmcgui.Dialog().ok(self.LB_LOGIN_ERROR, "GENERIC LOGIN ERROR")
            if len(REDIRECT_URL) > 0:
                xbmcgui.Dialog().ok(self.LB_ERROR, "OPERATOR WITH LOGIN REDIRECTION DETECTED. LOGIN REDIRECTION IS NOT CURRENTLY IMPLEMENTED. TO FIND OUT MORE ABOUTE THE ISSUE AND/OR CONTRIBUTE GO TO https://github.com/arvvoid/plugin.video.hbogoeu  ISSUE #5 ")
            self.logout()
            return
        self.sessionId = '00000000-0000-0000-0000-000000000000'
        try:
            self.sessionId = jsonrspl['SessionId']
        except:
            self.sessionId = '00000000-0000-0000-0000-000000000000'
        if self.sessionId == '00000000-0000-0000-0000-000000000000' or len(self.sessionId) != 36:
            xbmc.log(self.DEBUG_ID_STRING + "GENERIC LOGIN ERROR")
            xbmcgui.Dialog().ok(self.LB_LOGIN_ERROR, "GENERIC LOGIN ERROR")
            if len(REDIRECT_URL) > 0:
                xbmcgui.Dialog().ok(self.LB_ERROR, "OPERATOR WITH LOGIN REDIRECTION DETECTED. LOGIN REDIRECTION IS NOT CURRENTLY IMPLEMENTED. TO FIND OUT MORE ABOUTE THE ISSUE AND/OR CONTRIBUTE GO TO https://github.com/arvvoid/plugin.video.hbogoeu  ISSUE #5 ")
            self.logout()
            return
        else:
            self.goToken = jsonrspl['Token']
            self.GOcustomerId = jsonrspl['Customer']['Id']
            if self.sensitive_debug:
                xbmc.log(self.DEBUG_ID_STRING + "Login sucess - Token" + str(self.goToken))
                xbmc.log(self.DEBUG_ID_STRING + "Login sucess - Customer Id" + str(self.GOcustomerId))
                xbmc.log(self.DEBUG_ID_STRING + "Login sucess - Session Id" + str(self.sessionId))
            else:
                xbmc.log(self.DEBUG_ID_STRING + "Login sucess - Token  [OMITTED FOR PRIVACY]")
                xbmc.log(self.DEBUG_ID_STRING + "Login sucess - Customer Id  [OMITTED FOR PRIVACY]")
                xbmc.log(self.DEBUG_ID_STRING + "Login sucess - Session Id [OMITTED FOR PRIVACY]")
            self.loggedin_headers['GO-SessionId'] = str(self.sessionId)
            self.loggedin_headers['GO-Token'] = str(self.goToken)
            self.loggedin_headers['GO-CustomerId'] = str(self.GOcustomerId)
            # save the session with validity of n hours to not relogin every run of the add-on
            saved_session = {

                "hash": login_hash,
                "headers": self.loggedin_headers,
                "time": time.time()

            }
            if self.sensitive_debug:
                xbmc.log(self.DEBUG_ID_STRING + "SAVING SESSION: " + str(saved_session))
            else:
                xbmc.log(self.DEBUG_ID_STRING + "SAVING SESSION: [OMITTED FOR PRIVACY]")
            self.save_obj(saved_session, self.addon_id + "_session")



    def categories(self):
        if not self.chk_login():
            self.login()
        self.setDispCat("")
        self.addCat(self.addon.getSetting('OperatorName')+" [LOGOUT]", "[LOGOUT]", self.md + 'logout.png', 9)
        self.addCat(self.LB_SEARCH, self.LB_SEARCH, self.md + 'search.png', 4)

        if (self.FavoritesGroupId == ""):
            self.getFavoriteGroup()

        if (self.FavoritesGroupId != ""):
            self.addCat(self.LB_MYPLAYLIST, self.API_URL_CUSTOMER_GROUP + self.FavoritesGroupId + '/-/-/-/1000/-/-/false', self.md + 'FavoritesFolder.png', 1)

        jsonrsp = self.get_from_hbogo(self.API_URL_GROUPS)

        try:
            if jsonrsp['ErrorMessage']:
                xbmcgui.Dialog().ok(self.LB_ERROR, jsonrsp['ErrorMessage'])
        except:
            pass

        for cat in jsonrsp['Items']:
            self.addCat(cat['Name'].encode('utf-8', 'ignore'), cat['ObjectUrl'].replace('/0/{sort}/{pageIndex}/{pageSize}/0/0', '/0/0/1/1024/0/0'), self.md + 'DefaultFolder.png', 1)
        xbmcplugin.endOfDirectory(self.handle)

    def list(self, url):
        if not self.chk_login():
            self.login()
        xbmc.log(self.DEBUG_ID_STRING + "List: " + str(url))

        if not self.chk_login():
            self.login()

        jsonrsp = self.get_from_hbogo(url)

        try:
            if jsonrsp['ErrorMessage']:
                xbmcgui.Dialog().ok(self.LB_ERROR, jsonrsp['ErrorMessage'])
        except:
            pass
        # If there is a subcategory / genres
        if len(jsonrsp['Container']) > 1:
            for Container in range(0, len(jsonrsp['Container'])):
                self.addCat(jsonrsp['Container'][Container]['Name'].encode('utf-8', 'ignore'),
                       jsonrsp['Container'][Container]['ObjectUrl'], self.md + 'DefaultFolder.png', 1)
        else:
            for title in jsonrsp['Container'][0]['Contents']['Items']:
                if title['ContentType'] == 1 or title['ContentType'] == 3:  # 1=MOVIE/EXTRAS, 2=SERIES(serial), 3=SERIES(episode)
                    self.addLink(title, 5)
                else:
                    self.addDir(title, 2, "tvshow")
        xbmcplugin.endOfDirectory(self.handle)

    def season(self, url):
        if not self.chk_login():
            self.login()
        xbmc.log(self.DEBUG_ID_STRING + "Season: " + str(url))
        jsonrsp = self.get_from_hbogo(url)

        try:
            if jsonrsp['ErrorMessage']:
                xbmcgui.Dialog().ok(self.LB_ERROR, jsonrsp['ErrorMessage'])
        except:
            pass
        for season in jsonrsp['Parent']['ChildContents']['Items']:
            self.addDir(season, 3, "season")
        xbmcplugin.endOfDirectory(self.handle)

    def episode(self, url):
        if not self.chk_login():
            self.login()
        xbmc.log(self.DEBUG_ID_STRING + "Episode: " + str(url))
        jsonrsp = self.get_from_hbogo(url)

        try:
            if jsonrsp['ErrorMessage']:
                xbmcgui.Dialog().ok(self.LB_ERROR, jsonrsp['ErrorMessage'])
        except:
            pass

        for episode in jsonrsp['ChildContents']['Items']:
            self.addLink(episode, 5)
        xbmcplugin.endOfDirectory(self.handle)

    def search(self):
        if not self.chk_login():
            self.login()
        keyb = xbmc.Keyboard(self.search_string, self.LB_SEARCH_DESC)
        keyb.doModal()
        if (keyb.isConfirmed()):
            searchText = urllib.quote_plus(keyb.getText())
            if searchText == "":
                self.addCat(self.LB_SEARCH_NORES, self.LB_SEARCH_NORES, self.md + 'DefaultFolderBack.png', '')
            else:
                self.addon.setSetting('lastsearch', searchText)
                xbmc.log(self.DEBUG_ID_STRING + "Performing search: " + str(self.API_URL_SEARCH + searchText.decode('utf-8', 'ignore').encode('utf-8', 'ignore') + '/0'))
                jsonrsp = self.get_from_hbogo(self.API_URL_SEARCH + searchText.decode('utf-8', 'ignore').encode('utf-8', 'ignore') + '/0')
                xbmc.log(str(jsonrsp))

                try:
                    if jsonrsp['ErrorMessage']:
                        xbmc.log(self.DEBUG_ID_STRING + "Search Error: " + str(jsonrsp['ErrorMessage']))
                        xbmcgui.Dialog().ok(self.LB_ERROR, jsonrsp['ErrorMessage'])
                except:
                    pass

                br = 0
                for item in jsonrsp['Container'][0]['Contents']['Items']:
                    if item['ContentType'] == 1 or item['ContentType'] == 7 or item['ContentType'] == 3:  # 1,7=MOVIE/EXTRAS, 2=SERIES(serial), 3=SERIES(episode)
                        self.addLink(item, 5)
                    else:
                        self.addDir(item, 2, "tvshow")
                    br = br + 1
                if br == 0:
                    self.addCat(self.LB_SEARCH_NORES, self.LB_SEARCH_NORES, self.md + 'DefaultFolderBack.png', '')
        xbmcplugin.endOfDirectory(self.handle)

    def play(self, url, content_id):
        xbmc.log(self.DEBUG_ID_STRING + "Play: " + str(url))

        if not self.chk_login():
            self.login()
        op_id = self.addon.getSetting('OperatorId')
        purchase_payload = '<Purchase xmlns="go:v5:interop"><AllowHighResolution>true</AllowHighResolution><ContentId>' + content_id + '</ContentId><CustomerId>' + self.GOcustomerId + '</CustomerId><Individualization>' + self.individualization + '</Individualization><OperatorId>' + op_id + '</OperatorId><ClientInfo></ClientInfo><IsFree>false</IsFree><UseInteractivity>false</UseInteractivity></Purchase>'
        xbmc.log(self.DEBUG_ID_STRING + "Purchase payload: " + str(purchase_payload))
        purchase_headers = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Accept-Encoding': '',
            'Accept-Language': self.ACCEPT_LANGUAGE,
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'GO-CustomerId': str(self.GOcustomerId),
            'GO-requiredPlatform': self.GO_REQUIRED_PLATFORM,
            'GO-SessionId': str(self.sessionId),
            'GO-swVersion': self.GO_SW_VERSION,
            'GO-Token': str(self.goToken),
            'Host': self.API_HOST,
            'Referer': self.API_HOST_REFERER,
            'Origin': self.API_HOST_ORIGIN,
            'User-Agent': self.UA
        }
        xbmc.log(self.DEBUG_ID_STRING + "Requesting purchase: " + str(self.API_URL_PURCHASE))
        jsonrspp = self.send_purchase_hbogo(self.API_URL_PURCHASE, purchase_payload, purchase_headers)
        xbmc.log(self.DEBUG_ID_STRING + "Purchase response: " + str(jsonrspp))

        try:
            if jsonrspp['ErrorMessage']:
                xbmc.log(self.DEBUG_ID_STRING + "Purchase error: " + str(jsonrspp['ErrorMessage']))
                xbmcgui.Dialog().ok(self.LB_ERROR, jsonrspp['ErrorMessage'])
        except:
            pass

        MediaUrl = jsonrspp['Purchase']['MediaUrl'] + "/Manifest"
        xbmc.log(self.DEBUG_ID_STRING + "Media Url: " + str(jsonrspp['Purchase']['MediaUrl'] + "/Manifest"))
        PlayerSessionId = jsonrspp['Purchase']['PlayerSessionId']
        xbmc.log(self.DEBUG_ID_STRING + "PlayerSessionId: " + str(jsonrspp['Purchase']['PlayerSessionId']))
        x_dt_auth_token = jsonrspp['Purchase']['AuthToken']
        xbmc.log(self.DEBUG_ID_STRING + "Auth token: " + str(jsonrspp['Purchase']['AuthToken']))
        dt_custom_data = base64.b64encode("{\"userId\":\"" + self.GOcustomerId + "\",\"sessionId\":\"" + PlayerSessionId + "\",\"merchant\":\"hboeurope\"}")

        li = xbmcgui.ListItem(path=MediaUrl)
        license_headers = 'dt-custom-data=' + dt_custom_data + '&x-dt-auth-token=' + x_dt_auth_token + '&Origin=' + self.API_HOST_ORIGIN + '&Content-Type='
        license_key = self.LICENSE_SERVER + '|' + license_headers + '|R{SSM}|JBlicense'
        xbmc.log(self.DEBUG_ID_STRING + "Licence key: " + str(license_key))
        protocol = 'ism'
        drm = 'com.widevine.alpha'
        is_helper = inputstreamhelper.Helper(protocol, drm=drm)
        is_helper.check_inputstream()
        li.setProperty('inputstreamaddon', 'inputstream.adaptive')
        li.setProperty('inputstream.adaptive.manifest_type', protocol)
        li.setProperty('inputstream.adaptive.license_type', drm)
        li.setProperty('inputstream.adaptive.license_data', 'ZmtqM2xqYVNkZmFsa3Izag==')
        li.setProperty('inputstream.adaptive.license_key', license_key)
        xbmc.log(self.DEBUG_ID_STRING + "Play url: " + str(li))
        xbmcplugin.setResolvedUrl(self.handle, True, li)

    def addLink(self, title, mode):
        xbmc.log(self.DEBUG_ID_STRING + "Adding Link: " + str(title) + " MODE: " + str(mode))
        cid = title['ObjectUrl'].rsplit('/', 2)[1]

        plot = ""
        name = ""
        media_type = "movie"
        if title['ContentType'] == 1:  # 1=MOVIE/EXTRAS, 2=SERIES(serial), 3=SERIES(episode)
            name = title['Name'].encode('utf-8', 'ignore')
            if self.force_original_names:
                name = title['OriginalName'].encode('utf-8', 'ignore')
            filename = title['OriginalName'].encode('utf-8', 'ignore') + " (" + str(title['ProductionYear']) + ")"
            if self.force_scraper_names:
                name = filename
            plot = title['Abstract'].encode('utf-8', 'ignore')
            if 'AvailabilityTo' in title:
                if title['AvailabilityTo'] is not None:
                    plot = plot + ' ' + self.LB_FILM_UNTILL + ' ' + title['AvailabilityTo'].encode('utf-8', 'ignore')
        elif title['ContentType'] == 3:
            media_type = "episode"
            name = title['SeriesName'].encode('utf-8', 'ignore') + " - " + str(
                title['SeasonIndex']) + " " + self.LB_SEASON + ", " + self.LB_EPISODE + " " + str(title['Index'])
            if self.force_original_names:
                name = title['OriginalName'].encode('utf-8', 'ignore')
            filename = title['Tracking']['ShowName'].encode('utf-8', 'ignore') + " - S" + str(
                title['Tracking']['SeasonNumber']) + "E" + str(title['Tracking']['EpisodeNumber'])
            if self.force_scraper_names:
                name = filename
            plot = title['Abstract'].encode('utf-8', 'ignore')
            if 'AvailabilityTo' in title:
                plot = plot + ' ' + self.LB_EPISODE_UNTILL + ' ' + title['AvailabilityTo'].encode('utf-8', 'ignore')

        u = self.base_url + "?url=" + urllib.quote_plus(title['ObjectUrl']) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(filename) + "&cid=" + cid + "&thumbnail=" + title['BackgroundUrl']

        liz = xbmcgui.ListItem(name, iconImage=title['BackgroundUrl'], thumbnailImage=title['BackgroundUrl'])
        liz.setArt({'thumb': title['BackgroundUrl'], 'poster': title['BackgroundUrl'], 'banner': title['BackgroundUrl'],
                    'fanart': title['BackgroundUrl']})
        liz.setInfo(type="Video",
                    infoLabels={"mediatype": media_type, "episode": title['Tracking']['EpisodeNumber'],
                                "season": title['Tracking']['SeasonNumber'],
                                "tvshowtitle": title['Tracking']['ShowName'], "plot": plot,
                                "mpaa": str(title['AgeRating']) + '+', "rating": title['ImdbRate'],
                                "cast": [title['Cast'].split(', ')][0], "director": title['Director'],
                                "writer": title['Writer'], "duration": title['Duration'], "genre": title['Genre'],
                                "title": name, "originaltitle": title['OriginalName'],
                                "year": title['ProductionYear']})
        liz.addStreamInfo('video', {'width': 1920, 'height': 1080})
        liz.addStreamInfo('video', {'aspect': 1.78, 'codec': 'h264'})
        liz.addStreamInfo('audio', {'codec': 'aac', 'channels': 2})
        liz.setProperty("IsPlayable", "true")
        xbmcplugin.addDirectoryItem(handle=self.handle, url=u, listitem=liz, isFolder=False)


    def addDir(self, item, mode, media_type):
        xbmc.log(self.DEBUG_ID_STRING + "Adding Dir: " + str(item) + " MODE: " + str(mode))
        u = self.base_url + "?url=" + urllib.quote_plus(item['ObjectUrl']) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(item['OriginalName'].encode('utf-8', 'ignore') + " (" + str(item['ProductionYear']) + ")")
        liz = xbmcgui.ListItem(item['Name'].encode('utf-8', 'ignore'), iconImage=self.md + "DefaultFolder.png", thumbnailImage=item['BackgroundUrl'])
        liz.setInfo(type="Video", infoLabels={"mediatype": media_type, "season": item['Tracking']['SeasonNumber'],
                                              "tvshowtitle": item['Tracking']['ShowName'],
                                              "title": item['Name'].encode('utf-8', 'ignore'),
                                              "Plot": item['Abstract'].encode('utf-8', 'ignore')})
        liz.setProperty('isPlayable', "false")
        xbmcplugin.addDirectoryItem(handle=self.handle, url=u, listitem=liz, isFolder=True)


    def addCat(self, name, url, icon, mode):
        xbmc.log(self.DEBUG_ID_STRING + "Adding Cat: " + str(name) + "," + str(url) + "," + str(icon) + " MODE: " + str(mode))
        u = self.base_url + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
        liz = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
        liz.setInfo(type="Video", infoLabels={"Title": name})
        liz.setProperty('isPlayable', "false")
        xbmcplugin.addDirectoryItem(handle=self.handle, url=u, listitem=liz, isFolder=True)


