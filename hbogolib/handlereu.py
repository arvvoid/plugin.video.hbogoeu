# encoding: utf-8
# HboGo EU handler class for Hbo Go Kodi add-on
# Copyright (C) 2019 ArvVoid (https://github.com/arvvoid)
# Derived from version v.2.0-beta5 of the add-on, witch was initialy
# derived from https://github.com/billsuxx/plugin.video.hbogohu witch is
# derived from https://kodibg.org/forum/thread-504.html
# Oauth login/solution for providers with login redirection derived from https://github.com/kszaq/plugin.video.hbogopl
# Relesed under GPL version 2
#########################################################
# http://hbogo.eu HBOGO EU HANDLER CLASS
#########################################################


from hbogolib.handler import HbogoHandler
from hbogolib.constants import HbogoConstants

import sys
import time
import urllib
import json
import base64
import hashlib
import requests

try:
    import urllib.parse as parse
except ImportError:
    import urlparse as parse

import xbmc
import xbmcgui
import xbmcplugin
import inputstreamhelper

class HbogoHandler_eu(HbogoHandler):

    def __init__(self, handle, base_url, country):
        HbogoHandler.__init__(self, handle, base_url)
        self.operator_name = ""
        self.op_id = ""
        self.COUNTRY_CODE_SHORT = ""
        self.COUNTRY_CODE = ""
        self.DEFAULT_LANGUAGE = ""
        self.DOMAIN_CODE = ""
        self.is_web = True
        self.REDIRECT_URL = ""
        self.SPECIALHOST_URL= ""
        #GEN API URLS

        # API URLS
        self.LANGUAGE_CODE = self.DEFAULT_LANGUAGE

        self.LICENSE_SERVER = ""

        self.API_HOST = ""

        self.API_HOST_REFERER = ""
        self.API_HOST_ORIGIN = ""


        self.API_HOST_GATEWAY = ""
        self.API_HOST_GATEWAY_REFERER = ""

        self.API_URL_SETTINGS = ""
        self.API_URL_AUTH_WEBBASIC = ""
        self.API_URL_AUTH_OPERATOR = ""
        self.API_URL_CUSTOMER_GROUP = ""
        self.API_URL_GROUPS = ""
        self.API_URL_GROUPS_OLD = ""
        self.API_URL_CONTENT = ""
        self.API_URL_PURCHASE = ""
        self.API_URL_SEARCH = ""
        self.API_URL_ADD_RATING = ""
        self.API_URL_ADD_MYLIST = ""

        self.individualization = ""
        self.goToken = ""
        self.customerId = ""
        self.GOcustomerId = ""
        self.sessionId = '00000000-0000-0000-0000-000000000000'
        self.FavoritesGroupId = ""

        self.loggedin_headers = {}

        #check operator_id
        if len(self.addon.getSetting('operator_id')) == 0:
            self.setup(country)
        else:
            self.init_api(country)

    def init_api(self,country):
        self.operator_name = self.addon.getSetting('operator_name')
        self.log("OPERATOR: " + self.operator_name)
        self.op_id=self.addon.getSetting('operator_id')
        self.log("OPERATOR ID: " + self.op_id)
        self.COUNTRY_CODE_SHORT = country[2]
        self.log("OPERATOR COUNTRY_CODE_SHORT: " + self.COUNTRY_CODE_SHORT)
        self.COUNTRY_CODE = country[3]
        self.log("OPERATOR COUNTRY_CODE: " + self.COUNTRY_CODE)
        self.DEFAULT_LANGUAGE = country[4]
        self.log("DEFAULT HBO GO LANGUAGE: " + self.DEFAULT_LANGUAGE)
        self.DOMAIN_CODE = country[1]
        if self.addon.getSetting('operator_is_web') == 'true':
            self.is_web = True
        else:
            self.is_web = False
        self.log("WEB OPERATOR: " + str(self.is_web))
        self.REDIRECT_URL=self.addon.getSetting('operator_redirect_url')
        self.log("OPERATOR REDIRECT: " + str(self.REDIRECT_URL))
        self.SPECIALHOST_URL=country[5]
        self.log("OPERATOR SPECIAL HOST URL: " + str(self.SPECIALHOST_URL))
        #GEN API URLS

        # API URLS
        self.LANGUAGE_CODE = self.DEFAULT_LANGUAGE

        if self.language(30000) == 'ENG':  # only englih or the default language for the selected operator is allowed
            self.LANGUAGE_CODE = 'ENG'

        # check if default language is forced
        if self.addon.getSetting('deflang') == 'true':
            self.LANGUAGE_CODE = self.DEFAULT_LANGUAGE

        self.LICENSE_SERVER = 'https://lic.drmtoday.com/license-proxy-widevine/cenc/'

        self.API_HOST = self.COUNTRY_CODE_SHORT + 'api.hbogo.eu'

        if len(self.SPECIALHOST_URL)>0:
            self.API_HOST_REFERER = self.SPECIALHOST_URL
            self.API_HOST_ORIGIN = self.SPECIALHOST_URL
        else:
            self.API_HOST_REFERER = 'https://hbogo.' + self.DOMAIN_CODE + '/'
            self.API_HOST_ORIGIN = 'https://www.hbogo.' + self.DOMAIN_CODE

        self.API_HOST_GATEWAY = 'https://gateway.hbogo.eu'
        self.API_HOST_GATEWAY_REFERER = 'https://gateway.hbogo.eu/signin/form'

        self.API_URL_SETTINGS = 'https://' + self.API_HOST + '/v7/Settings/json/' + self.LANGUAGE_CODE + '/' + self.API_PLATFORM
        self.API_URL_AUTH_WEBBASIC = 'https://api.ugw.hbogo.eu/v3.0/Authentication/' + self.COUNTRY_CODE + '/JSON/' + self.LANGUAGE_CODE + '/' + self.API_PLATFORM
        self.API_URL_AUTH_OPERATOR = 'https://' + self.COUNTRY_CODE_SHORT + 'gwapi.hbogo.eu/v2.1/Authentication/json/' + self.LANGUAGE_CODE + '/' + self.API_PLATFORM
        self.API_URL_CUSTOMER_GROUP = 'https://' + self.API_HOST + '/v7/CustomerGroup/json/' + self.LANGUAGE_CODE + '/' + self.API_PLATFORM + '/'
        self.API_URL_GROUPS = 'http://' + self.API_HOST + '/v7/Groups/json/' + self.LANGUAGE_CODE + '/ANMO/0/True'
        self.API_URL_GROUPS_OLD = 'https://' + self.API_HOST + '/v5/Groups/json/' + self.LANGUAGE_CODE + '/'+ self.API_PLATFORM
        self.API_URL_CONTENT = 'http://' + self.API_HOST + '/v5/Content/json/' + self.LANGUAGE_CODE + '/' + self.API_PLATFORM + '/'
        self.API_URL_PURCHASE = 'https://' + self.API_HOST + '/v5/Purchase/Json/' + self.LANGUAGE_CODE + '/' + self.API_PLATFORM
        self.API_URL_SEARCH = 'https://' + self.API_HOST + '/v5/Search/Json/' + self.LANGUAGE_CODE + '/' + self.API_PLATFORM + '/'

        self.API_URL_ADD_RATING = 'https://' + self.API_HOST + '/v7/AddRating/json/' + self.LANGUAGE_CODE + '/' + self.API_PLATFORM + '/'
        self.API_URL_ADD_MYLIST = 'https://' + self.API_HOST + '/v7/AddWatchlist/json/' + self.LANGUAGE_CODE + '/' + self.API_PLATFORM + '/'
        self.API_URL_REMOVE_MYLIST = 'https://' + self.API_HOST + '/v7/RemoveWatchlist/json/' + self.LANGUAGE_CODE + '/' + self.API_PLATFORM + '/'

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

    def setup(self, country):
        #setup operator

        self.log("SHOWING OPERATORS FOR: " + str(country))

        url_basic_operator = 'https://api.ugw.hbogo.eu/v3.0/Operators/' + country[3] + '/JSON/' + country[4] + '/COMP'
        url_operators = 'https://' + country[2] + 'gwapi.hbogo.eu/v2.1/Operators/json/' + country[4] + '/COMP'

        json_basic_operators = requests.get(url_basic_operator).json()
        json_operators = requests.get(url_operators).json()

        op_list = []

        for operator in json_basic_operators['Items']:
            icon = self.resources + "icon.png"
            try:
                if len(operator['LogoUrl'])>0:
                    icon = operator['LogoUrl']
            except:
                pass

            web = 'true'
            try:
                if operator['Type'] == "D2_C":
                    web = 'true'
                else:
                    web = 'false'
            except:
                pass

            redirect_url = ""
            try:
                redirect_url = operator['RedirectionUrl']
            except:
                pass

            op_list.append([operator['Name'], operator['Id'], icon, web, redirect_url])
        for operator in json_operators['Items']:
            icon = self.resources + "icon.png"
            try:
                if len(operator['LogoUrl'])>0:
                    icon = operator['LogoUrl']
            except:
                pass

            web = 'false'

            redirect_url = ""
            try:
                redirect_url = operator['RedirectionUrl']
            except:
                pass

            op_list.append([operator['Name'], operator['Id'], icon, web, redirect_url])

        list = []

        # 0 - operator name
        # 1 - operator id
        # 2 - icon
        # 3 - is hbogo web or 3th party operator
        # 4 - login redirection url

        for o in op_list:
            list.append(xbmcgui.ListItem(label=o[0], iconImage=o[2]))

        index = xbmcgui.Dialog().select(self.language(30445).encode('utf-8'), list, useDetails=True)
        if index != -1:
            self.addon.setSetting('operator_id', op_list[index][1])
            self.addon.setSetting('operator_name', op_list[index][0])
            self.addon.setSetting('operator_is_web', op_list[index][3])
            self.addon.setSetting('operator_redirect_url', op_list[index][4])
            # OPERATOR SETUP DONE

            self.init_api(country)
            if self.inputCredentials():
                return True
            else:
                self.del_setup()
                xbmcgui.Dialog().ok(self.LB_ERROR, self.language(30444).encode('utf-8'))
                sys.exit()
                return False
        else:
            self.del_setup()
            sys.exit()
            return False

    def storeIndiv(self, indiv, custid):
        self.addon.setSetting('individualization', str(indiv))
        self.individualization = str(indiv)
        self.addon.setSetting('customerId', str(custid))
        self.customerId = str(custid)

    def storeFavgroup(self, favgroupid):
        self.FavoritesGroupId = self.addon.getSetting('FavoritesGroupId')
        if self.FavoritesGroupId == "":
            self.addon.setSetting('FavoritesGroupId', favgroupid)
            self.FavoritesGroupId = favgroupid

    def silentRegister(self):
        self.log("DEVICE REGISTRATION")
        import uuid
        try:
            indiv = str(uuid.uuid4())
            self.log("DEVICE REGISTRATION: INDIVIDUALIZATION: " + str(indiv))
            custid = str(uuid.uuid4())
            self.log("DEVICE REGISTRATION: CUSTOMER ID: " + str(custid))
            self.storeIndiv(indiv, custid)
        except:
            self.logout()
            self.log("DEVICE REGISTRATION: READ/STORE INDIVIDUALIZATION PROBLEM")
            return False

        self.log("DEVICE REGISTRATION: COMPLETED")
        return True

    def getFavoriteGroup(self):
        jsonrsp = self.get_from_hbogo(self.API_URL_SETTINGS)

        self.favgroupId = jsonrsp['FavoritesGroupId']
        self.storeFavgroup(self.favgroupId)

    def chk_login(self):
        return (self.loggedin_headers['GO-SessionId']!='00000000-0000-0000-0000-000000000000' and len(self.loggedin_headers['GO-Token'])!=0 and len(self.loggedin_headers['GO-CustomerId'])!=0)

    def logout(self):
        self.log("Loging out")
        self.del_login()
        self.goToken = ""
        self.GOcustomerId = ""
        self.sessionId = '00000000-0000-0000-0000-000000000000'
        self.loggedin_headers['GO-SessionId'] = str(self.sessionId)
        self.loggedin_headers['GO-Token'] = str(self.goToken)
        self.loggedin_headers['GO-CustomerId'] = str(self.GOcustomerId)

    def OAuthLogin(self, username, password):

        #Check if operator is supported
        
        if self.op_id in HbogoConstants.eu_redirect_login:
            # perform login

            self.log("Attempting OAuth login for: " + str(self.op_id))
            self.log("Urls and data: " + str(HbogoConstants.eu_redirect_login[self.op_id]))

            hbo_session = requests.session()

            hbo_session.headers.update({
                'Host': self.COUNTRY_CODE_SHORT+'gwapi.hbogo.eu',
                'User-Agent': self.UA,
                'Accept': 'application/json',
                'Accept-Language': self.ACCEPT_LANGUAGE,
                'Accept-Encoding': 'br, gzip, deflate',
                'Referer': 'https://gateway.hbogo.eu/signin/sso',
                'Content-Type': 'application/json',
                'GO-CustomerId': '00000000-0000-0000-0000-000000000000',
                'Origin': 'https://gateway.hbogo.eu',
                'Connection': 'keep-alive'
            })

            hbo_payload = {
                "Action": None,
                "AppLanguage": None,
                "ActivationCode": None,
                "AllowedContents": [],
                "AudioLanguage": None,
                "AutoPlayNext": False,
                "BirthYear": 0,
                "CurrentDevice": {
                    "AppLanguage": "",
                    "AutoPlayNext": False,
                    "Brand": "Chrome",
                    "CreatedDate": "",
                    "DeletedDate": "",
                    "Id": self.customerId,
                    "Individualization": self.individualization,
                    "IsDeleted": False,
                    "LastUsed": "",
                    "Modell": "71",
                    "Name": "",
                    "OSName": "Linux",
                    "OSVersion": "undefined",
                    "Platform": self.API_PLATFORM,
                    "SWVersion": "3.3.9.6418.2100",
                    "SubtitleSize": ""
                },
                "CustomerCode": "",
                "DebugMode": False,
                "DefaultSubtitleLanguage": None,
                "EmailAddress": "",
                "FirstName": "",
                "Gender": 0,
                "Id": "00000000-0000-0000-0000-000000000000",
                "IsAnonymus": True,
                "IsPromo": False,
                "Language": "",
                "LastName": "",
                "Nick": "",
                "NotificationChanges": 0,
                "OperatorId": "00000000-0000-0000-0000-000000000000",
                "OperatorName": "",
                "OperatorToken": "",
                "ParentalControl": {
                    "Active": False,
                    "Password": "",
                    "Rating": 0,
                    "ReferenceId": "00000000-0000-0000-0000-000000000000"
                },
                "Password": "",
                "PromoCode": "",
                "ReferenceId": "00000000-0000-0000-0000-000000000000",
                "SecondaryEmailAddress": "",
                "SecondarySpecificData": None,
                "ServiceCode": "",
                "SpecificData": None,
                "SubscribeForNewsletter": False,
                "SubscState": None,
                "SubtitleSize": "",
                "TVPinCode": "",
                "ZipCode": "",
                "PromoId": ""
            }

            hbo_session.headers.update({'GO-CustomerId': '00000000-0000-0000-0000-000000000000'})

            response = hbo_session.post(
                self.API_URL_AUTH_OPERATOR,
                json=hbo_payload
            )

            jsonrspl = response.json()

            token = str(jsonrspl['Token'])
            backuri = self.API_HOST_REFERER + "/ssocallbackhandler?ssoid={0}&method={1}&cou=POL&operatorId=" + self.op_id + "&p=" + self.API_PLATFORM + "&l=" + self.LANGUAGE_CODE + "&cb=" + base64.b64encode(token) + "&t=signin"

            hbo_session.headers.pop('GO-CustomerId')
            hbo_session.headers.update({'GO-Token': token})
            hbo_payload['CurrentDevice'] = jsonrspl['Customer']['CurrentDevice']
            hbo_payload['Action'] = 'L'
            hbo_payload['OperatorId'] = self.op_id

            cp_session = requests.session()
            cp_session.headers.update({
                'Referer': self.API_HOST_REFERER,
                'User-Agent': self.UA
            })


            payload = {
                "caller": "GW",
                "cid": str(jsonrspl['Customer']['Id']),
                "oid": self.op_id,
                "platform": self.API_PLATFORM,
                "backuri": backuri
            }

            self.log("GET CP SESSION: " + self.REDIRECT_URL.split('?')[0])

            cp_session.get(
                self.REDIRECT_URL.split('?')[0],
                params=payload
            )

            payload = HbogoConstants.eu_redirect_login[self.op_id][3]

            self.log("LOGIN FORM PAYLOAD: " + str(payload))

            payload[HbogoConstants.eu_redirect_login[self.op_id][1]] = username
            payload[HbogoConstants.eu_redirect_login[self.op_id][2]] = password

            if self.sensitive_debug:
                self.log("LOGIN FORM PAYLOAD: " + str(payload))

            response = cp_session.post(
                HbogoConstants.eu_redirect_login[self.op_id][0],
                data=payload
            )

            self.log("RESPONSE URL: " + str(response.url))

            parsed_url = parse.urlparse(response.url)

            self.log("PARTED URL: " + str(parsed_url))

            try:
                ssoid = parse.parse_qs(parsed_url.query)['ssoid'][0]
            except:
                self.log("OAuth login attempt failed, operator not supported: " + str(self.op_id))
                xbmcgui.Dialog().ok(self.LB_LOGIN_ERROR, "Sorry the OAuth login attempt have failed. Your operator require a special login procedure thats not supported at the moment. Please report with a full debug log")
                self.del_setup()
                self.log(str(response))
                sys.exit()

            response = hbo_session.post(
                'https://' + self.COUNTRY_CODE_SHORT +'gwapi.hbogo.eu/v2.1/RetrieveCustomerByToken/json/'+ self.LANGUAGE_CODE + '/' + self.API_PLATFORM
            )

            jsonrspl = response.json()

            hbo_session.headers.update({
                'GO-CustomerId': str(jsonrspl['Customer']['Id']),
                'GO-SessionId': str(jsonrspl['SessionId'])
            })

            hbo_payload['Id'] = str(jsonrspl['Customer']['Id'])
            hbo_payload['ReferenceId'] = ssoid

            response = hbo_session.post(
                self.API_URL_AUTH_OPERATOR,
                json=hbo_payload
            )

            jsonrspl = response.json()

            try:
                if jsonrspl['ErrorMessage']:
                    self.log("OAuth Login Error: " + str(str(jsonrspl['ErrorMessage'])))
                    xbmcgui.Dialog().ok(self.LB_LOGIN_ERROR, str(jsonrspl['ErrorMessage']))
                    self.logout()
                    return False
            except:
                pass

            try:
                if self.customerId != jsonrspl['Customer']['CurrentDevice']['Id'] or self.individualization != jsonrspl['Customer']['CurrentDevice']['Individualization']:
                    self.log("Device ID or Individualization Mismatch Showing diferences")
                    self.log("Device ID: " + self.customerId + " : " + jsonrspl['Customer']['CurrentDevice']['Id'])
                    self.log("Individualization: " + self.individualization + " : " + jsonrspl['Customer']['CurrentDevice']['Individualization'])
                    self.storeIndiv(jsonrspl['Customer']['CurrentDevice']['Individualization'],
                                    jsonrspl['Customer']['CurrentDevice']['Id'])
                else:
                    self.log("Device ID and Individualization Match")
            except:
                self.log("LOGIN: INDIVIDUALIZATION ERROR")
                xbmcgui.Dialog().ok(self.LB_LOGIN_ERROR, "LOGIN: INDIVIDUALIZATION ERROR")
                self.logout()
                return False

            try:
                self.sessionId = jsonrspl['SessionId']
            except:
                self.sessionId = '00000000-0000-0000-0000-000000000000'
            if self.sessionId == '00000000-0000-0000-0000-000000000000' or len(self.sessionId) != 36:
                self.log("GENERIC LOGIN ERROR")
                xbmcgui.Dialog().ok(self.LB_LOGIN_ERROR, "GENERIC LOGIN ERROR")
                self.logout()
                return False
            else:
                self.goToken = jsonrspl['Token']
                self.GOcustomerId = jsonrspl['Customer']['Id']
                if self.sensitive_debug:
                    self.log("Login sucess - Token" + str(self.goToken))
                    self.log("Login sucess - Customer Id" + str(self.GOcustomerId))
                    self.log("Login sucess - Session Id" + str(self.sessionId))
                else:
                    self.log("Login sucess - Token  [OMITTED FOR PRIVACY]")
                    self.log("Login sucess - Customer Id  [OMITTED FOR PRIVACY]")
                    self.log("Login sucess - Session Id [OMITTED FOR PRIVACY]")
                self.loggedin_headers['GO-SessionId'] = str(self.sessionId)
                self.loggedin_headers['GO-Token'] = str(self.goToken)
                self.loggedin_headers['GO-CustomerId'] = str(self.GOcustomerId)
                # save the session with validity of n hours to not relogin every run of the add-on

                login_hash = hashlib.sha224(self.individualization + self.customerId + self.FavoritesGroupId + username + password + self.op_id).hexdigest()
                self.log("LOGIN HASH: " + login_hash)

                saved_session = {

                    "hash": login_hash,
                    "headers": self.loggedin_headers,
                    "time": time.time()

                }
                if self.sensitive_debug:
                    self.log("SAVING SESSION: " + str(saved_session))
                else:
                    self.log("SAVING SESSION: [OMITTED FOR PRIVACY]")
                self.save_obj(saved_session, self.addon_id + "_session")
                return True
        else:
            self.log("OAuth operator not supported: " + str(self.op_id))
            xbmcgui.Dialog().ok(self.LB_LOGIN_ERROR, "Sorry your operator require a special login procedure thats not supported at the moment.")
        pass

    def login(self):
        self.log("Using operator: " + str(self.op_id))

        username = self.getCredential('username')
        password = self.getCredential('password')
        self.customerId = self.addon.getSetting('customerId')
        self.individualization = self.addon.getSetting('individualization')
        self.FavoritesGroupId = self.addon.getSetting('FavoritesGroupId')
        self.KidsGroupId = self.addon.getSetting('KidsGroupId')

        if (self.individualization == "" or self.customerId == ""):
            self.log("NO REGISTRED DEVICE - generating indivudualization and customer_id.")
            self.silentRegister()

        if (self.FavoritesGroupId == ""):
            self.getFavoriteGroup()

        if (username == "" or password == ""):
            xbmcgui.Dialog().ok(self.LB_LOGIN_ERROR, self.LB_NOLOGIN)
            self.addon.openSettings()
            sys.exit()
            return False

        login_hash = hashlib.sha224(self.individualization + self.customerId + self.FavoritesGroupId + username + password + self.op_id).hexdigest()
        self.log("LOGIN HASH: " + login_hash)

        loaded_session = self.load_obj(self.addon_id + "_session")

        if loaded_session is not None:
            # sesion exist if valid restore
            self.log("SAVED SESSION LOADED")
            if loaded_session["hash"] == login_hash:
                self.log("HASH IS VALID")
                if time.time() < (loaded_session["time"] + (self.SESSION_VALIDITY * 60 * 60)):
                    self.log("NOT EXPIRED RESTORING...")
                    # valid loaded sesion restor and exit login
                    if self.sensitive_debug:
                        self.log("Restoring login from saved: " + str(loaded_session))
                    else:
                        self.log("Restoring login from saved: [OMITTED FOR PRIVACY]")
                    self.loggedin_headers = loaded_session["headers"]
                    self.sessionId = self.loggedin_headers['GO-SessionId']
                    self.goToken = self.loggedin_headers['GO-Token']
                    self.GOcustomerId = self.loggedin_headers['GO-CustomerId']
                    if self.sensitive_debug:
                        self.log("Login restored - Token" + str(self.goToken))
                        self.log("Login restored - Customer Id" + str(self.GOcustomerId))
                        self.log("Login restored - Session Id" + str(self.sessionId))
                    else:
                        self.log("Login restored - Token  [OMITTED FOR PRIVACY]")
                        self.log("Login restored - Customer Id  [OMITTED FOR PRIVACY]")
                        self.log("Login restored - Session Id [OMITTED FOR PRIVACY]")
                    loaded_session['time'] = time.time()
                    if self.sensitive_debug:
                        self.log("REFRESHING SAVED SESSION: " + str(saved_session))
                    else:
                        self.log("REFRESHING SAVED SESSION: [OMITTED FOR PRIVACY]")
                    self.save_obj(loaded_session, self.addon_id + "_session")
                    return True

        if len(self.REDIRECT_URL) > 0:
            self.log("OPERATOR WITH LOGIN REDIRECTION DETECTED")
            self.log("LOGIN WITH SPECIAL OAuth LOGIN PROCEDURE")
            return self.OAuthLogin(username, password)


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

        if self.is_web:
            url = self.API_URL_AUTH_WEBBASIC
        else:
            url = self.API_URL_AUTH_OPERATOR

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
                "Brand": "Chrome",
                "CreatedDate": "",
                "DeletedDate": "",
                "Id": self.customerId,
                "Individualization": self.individualization,
                "IsDeleted": False,
                "LastUsed": "",
                "Modell": "71",
                "Name": "",
                "OSName": "Linux",
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
            "Nick": username,
            "NotificationChanges": 0,
            "OperatorId": self.op_id,
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
            self.log("PERFORMING LOGIN: " + str(data))
        else:
            self.log("PERFORMING LOGIN")
        jsonrspl = self.send_login_hbogo(url, headers, data)

        try:
            if jsonrspl['ErrorMessage']:
                self.log("LOGIN ERROR: " + str(jsonrspl['ErrorMessage']))
                xbmcgui.Dialog().ok(self.LB_LOGIN_ERROR, str(jsonrspl['ErrorMessage']))
                self.logout()
                return False
        except:
            pass

        try:
            if self.customerId != jsonrspl['Customer']['CurrentDevice']['Id'] or self.individualization != jsonrspl['Customer']['CurrentDevice']['Individualization']:
                self.log("Device ID or Individualization Mismatch Showing diferences")
                self.log("Device ID: " + self.customerId + " : " + jsonrspl['Customer']['CurrentDevice']['Id'])
                self.log("Individualization: " + self.individualization + " : " + jsonrspl['Customer']['CurrentDevice']['Individualization'])
                self.storeIndiv(jsonrspl['Customer']['CurrentDevice']['Individualization'], jsonrspl['Customer']['CurrentDevice']['Id'])
            else:
                self.log("Customer ID and Individualization Match")
        except:
            self.log("LOGIN: INDIVIDUALIZATION ERROR")
            xbmcgui.Dialog().ok(self.LB_LOGIN_ERROR, "LOGIN: INDIVIDUALIZATION ERROR")
            self.logout()
            return False
        self.sessionId = '00000000-0000-0000-0000-000000000000'
        try:
            self.sessionId = jsonrspl['SessionId']
        except:
            self.sessionId = '00000000-0000-0000-0000-000000000000'
        if self.sessionId == '00000000-0000-0000-0000-000000000000' or len(self.sessionId) != 36:
            self.log("GENERIC LOGIN ERROR")
            xbmcgui.Dialog().ok(self.LB_LOGIN_ERROR, "GENERIC LOGIN ERROR")
            self.logout()
            return False
        else:
            self.goToken = jsonrspl['Token']
            self.GOcustomerId = jsonrspl['Customer']['Id']
            if self.sensitive_debug:
                self.log("Login sucess - Token" + str(self.goToken))
                self.log("Login sucess - Customer Id" + str(self.GOcustomerId))
                self.log("Login sucess - Session Id" + str(self.sessionId))
            else:
                self.log("Login sucess - Token  [OMITTED FOR PRIVACY]")
                self.log("Login sucess - Customer Id  [OMITTED FOR PRIVACY]")
                self.log("Login sucess - Session Id [OMITTED FOR PRIVACY]")
            self.loggedin_headers['GO-SessionId'] = str(self.sessionId)
            self.loggedin_headers['GO-Token'] = str(self.goToken)
            self.loggedin_headers['GO-CustomerId'] = str(self.GOcustomerId)
            # save the session with validity of n hours to not relogin every run of the add-on

            login_hash = hashlib.sha224(self.individualization + self.customerId + self.FavoritesGroupId + username + password + self.op_id).hexdigest()
            self.log("LOGIN HASH: " + login_hash)

            saved_session = {

                "hash": login_hash,
                "headers": self.loggedin_headers,
                "time": time.time()

            }
            if self.sensitive_debug:
                self.log("SAVING SESSION: " + str(saved_session))
            else:
                self.log("SAVING SESSION: [OMITTED FOR PRIVACY]")
            self.save_obj(saved_session, self.addon_id + "_session")
            return True



    def categories(self):
        if not self.chk_login():
            self.login()
        self.setDispCat(self.operator_name)
        self.addCat(self.LB_SEARCH, self.LB_SEARCH, self.md + 'search.png', 4)

        if (self.FavoritesGroupId == ""):
            self.getFavoriteGroup()

        if (self.FavoritesGroupId != ""):
            self.addCat(self.LB_MYPLAYLIST, self.API_URL_CUSTOMER_GROUP + self.FavoritesGroupId + '/-/-/-/1000/-/-/false', self.md + 'FavoritesFolder.png', 1)

        jsonrsp = self.get_from_hbogo(self.API_URL_GROUPS)
        jsonrsp2 = self.get_from_hbogo(self.API_URL_GROUPS_OLD)

        try:
            if jsonrsp['ErrorMessage']:
                xbmcgui.Dialog().ok(self.LB_ERROR, jsonrsp['ErrorMessage'])
        except:
            pass

        position_home = -1
        position_series = -1
        position_movies = -1
        position_week_top = -1
        position_kids = -1

        position = 0

        # Find key categories positions
        try:
            for cat in jsonrsp['Items']:
                if cat["Tracking"]['Name'].encode('utf-8', 'ignore') == "Home":
                    position_home = position
                if cat["Tracking"]['Name'].encode('utf-8', 'ignore') == "Series":
                    position_series = position
                if cat["Tracking"]['Name'].encode('utf-8', 'ignore') == "Movies":
                    position_movies = position
                if position_home > -1 and position_series > -1 and position_movies > -1:
                    break
                position += 1
            position = 0
            for cat in jsonrsp2['Items']:
                if cat["Tracking"]['Name'].encode('utf-8', 'ignore') == "Weekly Top":
                    position_week_top = position
                if cat["Tracking"]['Name'].encode('utf-8', 'ignore') == "Kids":
                    position_kids = position
                if position_week_top > -1 and position_kids > -1:
                    break
                position += 1
        except:
            pass

        if position_series != -1:
            self.addCat(self.language(30716).encode('utf-8'), jsonrsp['Items'][position_series]['ObjectUrl'].replace('/0/{sort}/{pageIndex}/{pageSize}/0/0', '/0/0/1/1024/0/0'), self.md + 'tv.png', 1)
        else:
            self.log("No Series Category found")

        if position_movies != -1:
            self.addCat(self.language(30717).encode('utf-8'), jsonrsp['Items'][position_movies]['ObjectUrl'].replace('/0/{sort}/{pageIndex}/{pageSize}/0/0', '/0/0/1/1024/0/0'), self.md + 'movie.png', 1)
        else:
            self.log("No Movies Category found")

        if position_kids != -1:
            self.addCat(self.language(30729).encode('utf-8'), jsonrsp2['Items'][position_kids]['ObjectUrl'].replace('/0/{sort}/{pageIndex}/{pageSize}/0/0', '/0/0/1/1024/0/0'), self.md + 'kids.png', 1)
        else:
            self.log("No Kids Category found")

        if position_week_top != -1:
            self.addCat(self.language(30730).encode('utf-8'), jsonrsp2['Items'][position_week_top]['ObjectUrl'].replace('/0/{sort}/{pageIndex}/{pageSize}/0/0', '/0/0/1/1024/0/0'), self.md + 'DefaultFolder.png', 1)
        else:
            self.log("No Week Top Category found")

        if position_home != -1:
            self.list(jsonrsp['Items'][position_home]['ObjectUrl'].replace('/0/{sort}/{pageIndex}/{pageSize}/0/0', '/0/0/1/1024/0/0'), True)
        else:
            self.log("No Home Category found")

        xbmcplugin.addSortMethod(
            handle=self.handle,
            sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.endOfDirectory(self.handle)

    def list(self, url, simple=False):
        if not self.chk_login():
            self.login()
        self.log("List: " + str(url))

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
        if simple == False:
            xbmcplugin.addSortMethod(handle=self.handle, sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)
            xbmcplugin.addSortMethod(handle=self.handle, sortMethod=xbmcplugin.SORT_METHOD_LABEL)
            xbmcplugin.addSortMethod(handle=self.handle, sortMethod=xbmcplugin.SORT_METHOD_TITLE)
            xbmcplugin.addSortMethod(handle=self.handle, sortMethod=xbmcplugin.SORT_METHOD_VIDEO_YEAR)
            xbmcplugin.addSortMethod(handle=self.handle, sortMethod=xbmcplugin.SORT_METHOD_GENRE)
            xbmcplugin.addSortMethod(handle=self.handle, sortMethod=xbmcplugin.SORT_METHOD_LASTPLAYED)
            xbmcplugin.setContent(self.handle, self.use_content_type)
            xbmcplugin.endOfDirectory(self.handle)

    def season(self, url):
        if not self.chk_login():
            self.login()
        self.log("Season: " + str(url))
        jsonrsp = self.get_from_hbogo(url)

        try:
            if jsonrsp['ErrorMessage']:
                xbmcgui.Dialog().ok(self.LB_ERROR, jsonrsp['ErrorMessage'])
        except:
            pass
        for season in jsonrsp['Parent']['ChildContents']['Items']:
            self.addDir(season, 3, "season")
        xbmcplugin.addSortMethod(
            handle=self.handle,
            sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.addSortMethod(
            handle=self.handle,
            sortMethod=xbmcplugin.SORT_METHOD_LABEL)
        xbmcplugin.addSortMethod(
            handle=self.handle,
            sortMethod=xbmcplugin.SORT_METHOD_TITLE)
        xbmcplugin.addSortMethod(
            handle=self.handle,
            sortMethod=xbmcplugin.SORT_METHOD_VIDEO_YEAR)
        xbmcplugin.addSortMethod(
            handle=self.handle,
            sortMethod=xbmcplugin.SORT_METHOD_GENRE)
        xbmcplugin.addSortMethod(
            handle=self.handle,
            sortMethod=xbmcplugin.SORT_METHOD_LASTPLAYED)
        xbmcplugin.setContent(self.handle, self.use_content_type)
        xbmcplugin.endOfDirectory(self.handle)

    def episode(self, url):
        if not self.chk_login():
            self.login()
        self.log("Episode: " + str(url))
        jsonrsp = self.get_from_hbogo(url)

        try:
            if jsonrsp['ErrorMessage']:
                xbmcgui.Dialog().ok(self.LB_ERROR, jsonrsp['ErrorMessage'])
        except:
            pass

        for episode in jsonrsp['ChildContents']['Items']:
            self.addLink(episode, 5)
        xbmcplugin.addSortMethod(
            handle=self.handle,
            sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.addSortMethod(
            handle=self.handle,
            sortMethod=xbmcplugin.SORT_METHOD_LABEL)
        xbmcplugin.addSortMethod(
            handle=self.handle,
            sortMethod=xbmcplugin.SORT_METHOD_TITLE)
        xbmcplugin.addSortMethod(
            handle=self.handle,
            sortMethod=xbmcplugin.SORT_METHOD_VIDEO_YEAR)
        xbmcplugin.addSortMethod(
            handle=self.handle,
            sortMethod=xbmcplugin.SORT_METHOD_GENRE)
        xbmcplugin.addSortMethod(
            handle=self.handle,
            sortMethod=xbmcplugin.SORT_METHOD_LASTPLAYED)
        xbmcplugin.setContent(self.handle, self.use_content_type)
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
                self.log("Performing search: " + str(self.API_URL_SEARCH + searchText.decode('utf-8', 'ignore').encode('utf-8', 'ignore') + '/0'))
                jsonrsp = self.get_from_hbogo(self.API_URL_SEARCH + searchText.decode('utf-8', 'ignore').encode('utf-8', 'ignore') + '/0')
                self.log(str(jsonrsp))

                try:
                    if jsonrsp['ErrorMessage']:
                        self.log("Search Error: " + str(jsonrsp['ErrorMessage']))
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

        xbmcplugin.addSortMethod(
            handle=self.handle,
            sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.addSortMethod(
            handle=self.handle,
            sortMethod=xbmcplugin.SORT_METHOD_LABEL)
        xbmcplugin.addSortMethod(
            handle=self.handle,
            sortMethod=xbmcplugin.SORT_METHOD_TITLE)
        xbmcplugin.addSortMethod(
            handle=self.handle,
            sortMethod=xbmcplugin.SORT_METHOD_VIDEO_YEAR)
        xbmcplugin.addSortMethod(
            handle=self.handle,
            sortMethod=xbmcplugin.SORT_METHOD_GENRE)
        xbmcplugin.addSortMethod(
            handle=self.handle,
            sortMethod=xbmcplugin.SORT_METHOD_LASTPLAYED)
        xbmcplugin.setContent(self.handle, self.use_content_type)
        xbmcplugin.endOfDirectory(self.handle)

    def play(self, url, content_id):
        self.log("Play: " + str(url))

        if not self.chk_login():
            self.login()
        if not self.chk_login():
            self.log("NO LOGED IN ABORTING PLAY")
            xbmcgui.Dialog().ok(self.LB_LOGIN_ERROR, self.language(30103).encode('utf-8'))
            self.logout()
            return
        purchase_payload = '<Purchase xmlns="go:v5:interop"><AllowHighResolution>true</AllowHighResolution><ContentId>' + content_id + '</ContentId><CustomerId>' + self.GOcustomerId + '</CustomerId><Individualization>' + self.individualization + '</Individualization><OperatorId>' + self.op_id + '</OperatorId><ClientInfo></ClientInfo><IsFree>false</IsFree><UseInteractivity>false</UseInteractivity></Purchase>'
        self.log("Purchase payload: " + str(purchase_payload))
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
        self.log("Requesting purchase: " + str(self.API_URL_PURCHASE))
        jsonrspp = self.send_purchase_hbogo(self.API_URL_PURCHASE, purchase_payload, purchase_headers)
        self.log("Purchase response: " + str(jsonrspp))

        try:
            if jsonrspp['ErrorMessage']:
                self.log("Purchase error: " + str(jsonrspp['ErrorMessage']))
                xbmcgui.Dialog().ok(self.LB_ERROR, jsonrspp['ErrorMessage'])
                self.logout()
                return
        except:
            pass

        MediaUrl = jsonrspp['Purchase']['MediaUrl'] + "/Manifest"
        self.log("Media Url: " + str(jsonrspp['Purchase']['MediaUrl'] + "/Manifest"))
        PlayerSessionId = jsonrspp['Purchase']['PlayerSessionId']
        self.log("PlayerSessionId: " + str(jsonrspp['Purchase']['PlayerSessionId']))
        x_dt_auth_token = jsonrspp['Purchase']['AuthToken']
        self.log("Auth token: " + str(jsonrspp['Purchase']['AuthToken']))
        dt_custom_data = base64.b64encode("{\"userId\":\"" + self.GOcustomerId + "\",\"sessionId\":\"" + PlayerSessionId + "\",\"merchant\":\"hboeurope\"}")

        li = xbmcgui.ListItem(path=MediaUrl)
        license_headers = 'dt-custom-data=' + dt_custom_data + '&x-dt-auth-token=' + x_dt_auth_token + '&Origin=' + self.API_HOST_ORIGIN + '&Content-Type='
        license_key = self.LICENSE_SERVER + '|' + license_headers + '|R{SSM}|JBlicense'
        self.log("Licence key: " + str(license_key))
        protocol = 'ism'
        drm = 'com.widevine.alpha'
        is_helper = inputstreamhelper.Helper(protocol, drm=drm)
        is_helper.check_inputstream()
        li.setProperty('inputstreamaddon', 'inputstream.adaptive')
        li.setProperty('inputstream.adaptive.manifest_type', protocol)
        li.setProperty('inputstream.adaptive.license_type', drm)
        li.setProperty('inputstream.adaptive.license_data', 'ZmtqM2xqYVNkZmFsa3Izag==')
        li.setProperty('inputstream.adaptive.license_key', license_key)
        self.log("Play url: " + str(li))
        xbmcplugin.setResolvedUrl(self.handle, True, li)

    def procContext(self, type, content_id, optional=""):
        if not self.chk_login():
            self.login()

        icon = self.resources + "icon.png"

        if type == 9:
            resp = self.get_from_hbogo(self.API_URL_ADD_MYLIST + content_id)
            try:
                if resp["Success"]:
                    self.log("ADDED TO MY LIST: " + content_id)
                    xbmcgui.Dialog().notification(self.language(30719).encode('utf-8'), self.LB_SUCESS, icon)
                else:
                    self.log("FAILED ADD TO MY LIST: " + content_id)
                    xbmcgui.Dialog().notification(self.language(30719).encode('utf-8'), self.LB_ERROR, icon)
            except:
                self.log("ERROR ADD TO MY LIST: " + content_id)
                xbmcgui.Dialog().notification(self.language(30719).encode('utf-8'), self.LB_ERROR, icon)

        if type == 10:
            resp = self.get_from_hbogo(self.API_URL_REMOVE_MYLIST + content_id)
            try:
                if resp["Success"]:
                    self.log("REMOVED FROM MY LIST: " + content_id)
                    xbmcgui.Dialog().notification(self.language(30720).encode('utf-8'), self.LB_SUCESS, icon)
                    return xbmc.executebuiltin('Container.Refresh')
                else:
                    self.log("FAILED TO REMOVE MY LIST: " + content_id)
                    xbmcgui.Dialog().notification(self.language(30720).encode('utf-8'), self.LB_ERROR, icon)
            except:
                self.log("ERROR REMOVE FROM MY LIST: " + content_id)
                xbmcgui.Dialog().notification(self.language(30720).encode('utf-8'), self.LB_ERROR, icon)

        if type == 8:
            resp = self.get_from_hbogo(self.API_URL_ADD_RATING + content_id + '/' + optional)
            try:
                if resp["Success"]:
                    self.log("ADDED RATING: " + content_id + " " + optional)
                    xbmcgui.Dialog().notification(self.language(30726).encode('utf-8'), self.LB_SUCESS, icon)
                else:
                    self.log("FAILED RATING: " + content_id + " " + optional)
                    xbmcgui.Dialog().notification(self.language(30726).encode('utf-8'), self.LB_ERROR, icon)
            except:
                self.log("ERROR RATING: " + content_id + " " + optional)
                xbmcgui.Dialog().notification(self.language(30726).encode('utf-8'), self.LB_ERROR, icon)



    def genContextMenu(self, content_id, media_id):

        add_mylist = (self.language(30719).encode('utf-8'), 'RunPlugin(' + self.base_url + "?url=ADDMYLIST&mode=9&cid=" + media_id + ')')
        remove_mylist = (self.language(30720).encode('utf-8'), 'RunPlugin(' + self.base_url + "?url=REMMYLIST&mode=10&cid=" + media_id + ')')

        vote_5 = (self.language(30721).encode('utf-8'), 'RunPlugin(' + self.base_url + "?url=VOTE&mode=8&vote=5&cid=" + content_id + ')')
        vote_4 = (self.language(30722).encode('utf-8'), 'RunPlugin(' + self.base_url + "?url=VOTE&mode=8&vote=4&cid=" + content_id + ')')
        vote_3 = (self.language(30723).encode('utf-8'), 'RunPlugin(' + self.base_url + "?url=VOTE&mode=8&vote=3&cid=" + content_id + ')')
        vote_2 = (self.language(30724).encode('utf-8'), 'RunPlugin(' + self.base_url + "?url=VOTE&mode=8&vote=2&cid=" + content_id + ')')
        vote_1 = (self.language(30725).encode('utf-8'), 'RunPlugin(' + self.base_url + "?url=VOTE&mode=8&vote=1&cid=" + content_id + ')')

        if self.cur_loc == self.LB_MYPLAYLIST:
            return [vote_5, vote_4, vote_3, vote_2, vote_1, remove_mylist]
        else:
            return [add_mylist, vote_5, vote_4, vote_3, vote_2, vote_1]

    def addLink(self, title, mode):
        self.log("Adding Link: " + str(title) + " MODE: " + str(mode))
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
            if 'Description' in title:
                if title['Description'] is not None:
                    plot = title['Description'].encode('utf-8', 'ignore')
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
            if 'Description' in title:
                if title['Description'] is not None:
                    plot = title['Description'].encode('utf-8', 'ignore')
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
        if title['ContentType'] == 1:
            media_id = cid
            try:
                media_id = title['Id']
            except:
                pass
            liz.addContextMenuItems(items=self.genContextMenu(cid, media_id))
        xbmcplugin.addDirectoryItem(handle=self.handle, url=u, listitem=liz, isFolder=False)

    def addDir(self, item, mode, media_type):
        self.log("Adding Dir: " + str(item) + " MODE: " + str(mode))
        u = self.base_url + "?url=" + urllib.quote_plus(item['ObjectUrl']) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(item['OriginalName'].encode('utf-8', 'ignore') + " (" + str(item['ProductionYear']) + ")")
        liz = xbmcgui.ListItem(item['Name'].encode('utf-8', 'ignore'), iconImage=item['BackgroundUrl'], thumbnailImage=item['BackgroundUrl'])
        liz.setArt({'thumb': item['BackgroundUrl'], 'poster': item['BackgroundUrl'], 'banner': item['BackgroundUrl'],
                    'fanart': item['BackgroundUrl']})
        plot = item['Abstract'].encode('utf-8', 'ignore')
        if 'Description' in item:
            if item['Description'] is not None:
                plot = item['Description'].encode('utf-8', 'ignore')
        liz.setInfo(type="Video", infoLabels={"mediatype": media_type, "season": item['Tracking']['SeasonNumber'],
                                              "tvshowtitle": item['Tracking']['ShowName'],
                                              "title": item['Name'].encode('utf-8', 'ignore'),
                                              "Plot": plot})
        liz.setProperty('isPlayable', "false")
        if media_type == "tvshow":
            cid = item['ObjectUrl'].rsplit('/', 2)[1]
            media_id = cid
            try:
                media_id = item['SeriesId']
            except:
                pass
            liz.addContextMenuItems(items=self.genContextMenu(cid, media_id))
        xbmcplugin.addDirectoryItem(handle=self.handle, url=u, listitem=liz, isFolder=True)


    def addCat(self, name, url, icon, mode):
        self.log("Adding Cat: " + str(name) + "," + str(url) + "," + str(icon) + " MODE: " + str(mode))
        u = self.base_url + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
        liz = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
        liz.setArt({'fanart': self.resources + "fanart.jpg"})
        liz.setInfo(type="Video", infoLabels={"Title": name})
        liz.setProperty('isPlayable', "false")
        xbmcplugin.addDirectoryItem(handle=self.handle, url=u, listitem=liz, isFolder=True)


