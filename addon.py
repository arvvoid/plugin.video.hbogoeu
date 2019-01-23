# -*- coding: utf-8 -*-

import base64
import json
import sys
import urllib
import requests
import inputstreamhelper
import urllib2
import xbmc
import xbmcaddon
import xbmcgui
import xbmcplugin

__addon_id__ = 'plugin.video.hbogoeu'
__Addon = xbmcaddon.Addon(__addon_id__)
__settings__ = xbmcaddon.Addon(id='plugin.video.hbogoeu')
__language__ = __settings__.getLocalizedString

UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
MUA = 'Dalvik/2.1.0 (Linux; U; Android 8.0.0; Nexus 5X Build/OPP3.170518.006)'

md = xbmc.translatePath(__Addon.getAddonInfo('path') + "/resources/media/")
search_string = urllib.unquote_plus(__settings__.getSetting('lastsearch'))

# LABELS

LB_SEARCH_DESC = __language__(33700).encode('utf-8')
LB_SEARCH_NORES = __language__(33701).encode('utf-8')
LB_ERROR = __language__(33702).encode('utf-8')
LB_EPIZODE_UNTILL = __language__(33703).encode('utf-8')
LB_FILM_UNTILL = __language__(33704).encode('utf-8')
LB_EPISODE = __language__(33705).encode('utf-8')
LB_SEASON = __language__(33706).encode('utf-8')
LB_MYPLAYLIST = __language__(33707).encode('utf-8')
LB_NOLOGIN = __language__(33708).encode('utf-8')
LB_LOGIN_ERROR = __language__(33709).encode('utf-8')
LB_NO_OPERATOR = __language__(33710).encode('utf-8')
LB_SEARCH = __language__(33711).encode('utf-8')

operator = __settings__.getSetting('operator')
if operator == 'N/A':
    xbmcgui.Dialog().ok(LB_ERROR, LB_NO_OPERATOR)
    xbmcaddon.Addon(id='plugin.video.hbogoeu').openSettings()
    xbmc.executebuiltin("Action(Back)")
    sys.exit()
# 'operator SETTING_ID - > operator hash, short country code, long country code, country hash,web true/false
xbmc.log("OPERATOR SETTING_ID: " + operator)

op_ids = {
    'N/A': ['00000000-0000-0000-0000-000000000000', 'hr', 'HRV', 'ENG', '00000000-0000-0000-0000-000000000000', True],
    'Hungary: hbogo.hu (web registration)': ['15276cb7-7f53-432a-8ed5-a32038614bbf', 'hu', 'HUN', 'HUN', 'd35eda69-a367-4b47-aa0c-a51032d94be2', True],
    'Hungary: UPC Direct': ['48f48c5b-e9e4-4fca-833b-2fa26fb1ad22', 'hu', 'HUN', 'HUN', 'd35eda69-a367-4b47-aa0c-a51032d94be2', False],
    'Hungary: DIGI': ['b7728684-13d5-46d9-a9a4-97d676cdaeec', 'hu', 'HUN', 'HUN', 'd35eda69-a367-4b47-aa0c-a51032d94be2',False],
    'Hungary: Magyar Telekom Nyrt.': ['04459649-8a90-46f1-9390-0cd5b1958a5d', 'hu', 'HUN', 'HUN', 'd35eda69-a367-4b47-aa0c-a51032d94be2', False],
    'Hungary: Telenor MyTV': ['e71fabae-66b6-4972-9823-8743f8fcf06f', 'hu', 'HUN', 'HUN', 'd35eda69-a367-4b47-aa0c-a51032d94be2', False],
    'Hungary: UPC Magyarorszag': ['1ca45800-464a-4e9c-8f15-8d822ad7d8a1', 'hu', 'HUN', 'HUN','d35eda69-a367-4b47-aa0c-a51032d94be2', False],
    'Hungary: INVITEL': ['f2230905-8e25-4245-80f9-fccf67a24005', 'hu', 'HUN', 'HUN', 'd35eda69-a367-4b47-aa0c-a51032d94be2',False],
    'Hungary: Celldomolki Kabeltelevízió Kft.': ['383cd446-06fb-4a59-8d39-200a3e9bcf6f', 'hu', 'HUN', 'HUN', 'd35eda69-a367-4b47-aa0c-a51032d94be2', False],
    'Hungary: Eurocable - Hello Digital': ['fe106c75-293b-42e6-b211-c7446835b548', 'hu', 'HUN', 'HUN', 'd35eda69-a367-4b47-aa0c-a51032d94be2', False],
    'Hungary: hFC-Network Kft.': ['42677aa5-7576-4dc7-9004-347b279e4e5d', 'hu', 'HUN', 'HUN', 'd35eda69-a367-4b47-aa0c-a51032d94be2', False],
    'Hungary: HIR-SAT 2000 Kft.': ['3a3cce31-fb19-470a-9bb5-6947c4ac9996', 'hu', 'HUN', 'HUN', 'd35eda69-a367-4b47-aa0c-a51032d94be2', False],
    'Hungary: Jurop Telekom': ['c6441ec8-e30f-44b6-837a-beb2eb971395', 'hu', 'HUN', 'HUN', 'd35eda69-a367-4b47-aa0c-a51032d94be2', False],
    'Hungary: Kabelszat 2002': ['d91341c2-3542-40d4-adab-40b644798327', 'hu', 'HUN', 'HUN', 'd35eda69-a367-4b47-aa0c-a51032d94be2', False],
    'Hungary: Klapka Lakasszövetkezet': ['18fb0ff5-9cfa-4042-be00-638c5d34e553', 'hu', 'HUN', 'HUN', 'd35eda69-a367-4b47-aa0c-a51032d94be2', False],
    'Hungary: Lat-Sat Kft.': ['97cddb59-79e3-4090-be03-89a6ae06f5ec', 'hu', 'HUN', 'HUN', 'd35eda69-a367-4b47-aa0c-a51032d94be2', False],
    'Hungary: MinDig TV Extra': ['c48c350f-a9db-4eb6-97a6-9b659e2db47f', 'hu', 'HUN', 'HUN', 'd35eda69-a367-4b47-aa0c-a51032d94be2', False],
    'Hungary: PARISAT': ['7982d5c7-63df-431d-806e-54f98fdfa36a', 'hu', 'HUN', 'HUN', 'd35eda69-a367-4b47-aa0c-a51032d94be2', False],
    'Hungary: PR-TELECOM': ['18f536a3-ecac-42f1-91f1-2bbc3e6cfe81', 'hu', 'HUN', 'HUN', 'd35eda69-a367-4b47-aa0c-a51032d94be2', False],
    'Hungary: TARR Kft': ['adb99277-3899-439e-8bdf-c749c90493cd', 'hu', 'HUN', 'HUN', 'd35eda69-a367-4b47-aa0c-a51032d94be2', False],
    'Hungary: Vac Varosi Kabeltelevizio Kft.': ['5729f013-f01d-4cc3-b048-fe5c91c64296', 'hu', 'HUN', 'HUN', 'd35eda69-a367-4b47-aa0c-a51032d94be2', False],
    'Hungary: Vidanet Zrt.': ['b4f422f7-5424-4116-b72d-7cede85ead4e', 'hu', 'HUN', 'HUN', 'd35eda69-a367-4b47-aa0c-a51032d94be2', False],
    'Hungary: HBO Development Hungary': ['6a52efe0-54c4-4197-8c55-86ee7a63cd04', 'hu', 'HUN', 'HUN', 'd35eda69-a367-4b47-aa0c-a51032d94be2', False],
    'Hungary: HBO GO Vip/Club Hungary': ['f320aa2c-e40e-49c2-8cdd-1ebef2ac6f26', 'hu', 'HUN', 'HUN', 'd35eda69-a367-4b47-aa0c-a51032d94be2', False],
    'Croatia: hbogo.hr (web registration)': ['24a5e09c-4550-4cd3-a63c-8f6ab0508dd7', 'hr', 'HRV', 'HRV', '467fecfe-a523-43aa-9d9e-8522358a8ba4', True],
    'Croatia: A1': ['e1fb87d0-7581-4671-94bb-8e647e13385a', 'hr', 'HRV', 'HRV', '467fecfe-a523-43aa-9d9e-8522358a8ba4', False],
    'Croatia: BonBon': ['81a65859-145b-4bbc-afa6-04e9ade004f9', 'hr', 'HRV', 'HRV', '467fecfe-a523-43aa-9d9e-8522358a8ba4', False],
    'Croatia: evoTv': ['beed025d-06c9-4cac-a8a4-a118bdf22861', 'hr', 'HRV', 'HRV', '467fecfe-a523-43aa-9d9e-8522358a8ba4', False],
    'Croatia: HBO GO Vip/Club Croatia': ['323f061a-34e9-4453-987b-99aa38c46480', 'hr', 'HRV', 'HRV', '467fecfe-a523-43aa-9d9e-8522358a8ba4', False],
    'Croatia: Hrvatski Telekom d.d.': ['73893614-eae3-4435-ab53-1d46c7f90498', 'hr', 'HRV', 'HRV', '467fecfe-a523-43aa-9d9e-8522358a8ba4', False],
    'Croatia: Iskon Internet d.d.': ['5bff83d2-9163-4d85-9ae1-b6c2a6eabf71', 'hr', 'HRV', 'HRV', '467fecfe-a523-43aa-9d9e-8522358a8ba4', False],
    'Croatia: Optima Telekom d.d.': ['a9e06fc5-c8d3-4b79-a776-b78d86729843', 'hr', 'HRV', 'HRV', '467fecfe-a523-43aa-9d9e-8522358a8ba4', False],
    'Croatia: Simpa': ['3a1bb01c-9f7b-4029-a98d-6d17708fa4db', 'hr', 'HRV', 'HRV', '467fecfe-a523-43aa-9d9e-8522358a8ba4',False],
}
op_id = op_ids[operator][0]
xbmc.log("OPERATOR ID: " + op_id)

COUNTRY_ID = op_ids[operator][4]
xbmc.log("OPERATOR COUNTRY_ID: " + op_ids[operator][4])
COUNTRY_CODE_SHORT = op_ids[operator][1]
xbmc.log("OPERATOR COUNTRY_CODE_SHORT: " + op_ids[operator][1])
COUNTRY_CODE = op_ids[operator][2]
xbmc.log("OPERATOR COUNTRY_CODE: " + op_ids[operator][2])
IS_WEB = op_ids[operator][5]
xbmc.log("OPERATOR IS HBO GO WEB: " + str(IS_WEB))
DEFAULT_LANGUAGE = op_ids[operator][3]
xbmc.log("DEFAULT HBO GO LANGUAGE: " + DEFAULT_LANGUAGE)

# API URLS
LANGUAGE_CODE = DEFAULT_LANGUAGE

if __language__(32000) == 'ENG':  # only englih or the default language for the selected operator is allowed
    LANGUAGE_CODE = 'ENG'

#check if default language is forced
if __settings__.getSetting('deflang') == 'true':
    LANGUAGE_CODE = DEFAULT_LANGUAGE

API_PLATFORM = 'COMP'
# API_PLATFORM = 'MOBI'
# API_PLATFORM = 'APPLE'
# API_PLATFORM = 'SONY'

LICENSE_SERVER = 'https://lic.drmtoday.com/license-proxy-widevine/cenc/'

API_HOST = COUNTRY_CODE_SHORT + 'api.hbogo.eu'
API_HOST_REFERER = 'https://hbogo.' + COUNTRY_CODE_SHORT + '/'
API_HOST_ORIGIN = 'https://www.hbogo.' + COUNTRY_CODE_SHORT
API_HOST_GATEWAY = 'https://gateway.hbogo.eu'
API_HOST_GATEWAY_REFERER = 'https://gateway.hbogo.eu/signin/form'

API_URL_SILENTREGISTER = 'https://' + COUNTRY_CODE_SHORT + '.hbogo.eu/services/settings/silentregister.aspx'

API_URL_SETTINGS = 'https://' + API_HOST + '/v7/Settings/json/' + LANGUAGE_CODE + '/'+API_PLATFORM
API_URL_AUTH_WEBBASIC = 'https://api.ugw.hbogo.eu/v3.0/Authentication/' + COUNTRY_CODE + '/JSON/' + LANGUAGE_CODE + '/'+API_PLATFORM
API_URL_AUTH_OPERATOR = 'https://' + COUNTRY_CODE_SHORT + 'gwapi.hbogo.eu/v2.1/Authentication/json/' + LANGUAGE_CODE + '/'+API_PLATFORM
API_URL_CUSTOMER_GROUP = 'https://' + API_HOST + '/v7/CustomerGroup/json/' + LANGUAGE_CODE + '/' + API_PLATFORM + '/'
API_URL_GROUPS = 'https://' + API_HOST + '/v5/Groups/json/' + LANGUAGE_CODE + '/'+API_PLATFORM
API_URL_CONTENT='http://'+API_HOST+'/v5/Content/json/'+LANGUAGE_CODE + '/' + API_PLATFORM + '/'
API_URL_PURCHASE = 'https://' + API_HOST + '/v5/Purchase/Json/' + LANGUAGE_CODE + '/'+API_PLATFORM
API_URL_SEARCH = 'https://' + API_HOST + '/v5/Search/Json/' + LANGUAGE_CODE + '/' + API_PLATFORM + '/'

individualization = ""
goToken = ""
customerId = ""
GOcustomerId = ""
sessionId = '00000000-0000-0000-0000-000000000000'
FavoritesGroupId = ""

loggedin_headers = {
    'User-Agent': UA,
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': API_HOST_REFERER,
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'Origin': API_HOST_ORIGIN,
    'X-Requested-With': 'XMLHttpRequest',
    'GO-Language': LANGUAGE_CODE,
    'GO-requiredPlatform': 'CHBR',
    'GO-Token': '',
    'GO-SessionId': '',
    'GO-swVersion': '4.8.0',
    'GO-CustomerId': '',
    'Connection': 'keep-alive',
    'Accept-Encoding': ''
}


def storeIndiv(indiv, custid):
    global individualization
    global customerId

    individualization = __settings__.getSetting('individualization')
    if individualization == "":
        __settings__.setSetting('individualization', indiv)
        individualization = indiv

    customerId = __settings__.getSetting('customerId')
    if customerId == "":
        __settings__.setSetting('customerId', custid)
        customerId = custid


# FavoritesGroupId
def storeFavgroup(favgroupid):
    global FavoritesGroupId

    FavoritesGroupId = __settings__.getSetting('FavoritesGroupId')
    if FavoritesGroupId == "":
        __settings__.setSetting('FavoritesGroupId', favgroupid)
        FavoritesGroupId = favgroupid


# silent registration
def SILENTREGISTER():
    global goToken
    global individualization
    global customerId
    global sessionId

    req = urllib2.Request(API_URL_SILENTREGISTER, None, loggedin_headers)

    opener = urllib2.build_opener()
    f = opener.open(req)
    jsonrsp = json.loads(f.read())

    if jsonrsp['Data']['ErrorMessage']:
        xbmcgui.Dialog().ok(LB_ERROR, jsonrsp['Data']['ErrorMessage'])

    indiv = jsonrsp['Data']['Customer']['CurrentDevice']['Individualization']
    custid = jsonrsp['Data']['Customer']['CurrentDevice']['Id'];
    storeIndiv(indiv, custid)

    sessionId = jsonrsp['Data']['SessionId']
    return jsonrsp


def GETFAVORITEGROUP():
    global FavoritesGroupId

    req = urllib2.Request(API_URL_SETTINGS, None, loggedin_headers)

    opener = urllib2.build_opener()
    f = opener.open(req)
    jsonrsp = json.loads(f.read())

    favgroupId = jsonrsp['FavoritesGroupId']
    storeFavgroup(favgroupId)


# belepes
def LOGIN():
    global sessionId
    global goToken
    global customerId
    global GOcustomerId
    global individualization
    global loggedin_headers
    global FavoritesGroupId

    username = __settings__.getSetting('username')
    password = __settings__.getSetting('password')
    customerId = __settings__.getSetting('customerId')
    individualization = __settings__.getSetting('individualization')
    FavoritesGroupId = __settings__.getSetting('FavoritesGroupId')

    if (individualization == "" or customerId == ""):
      jsonrsp = SILENTREGISTER()

    if (FavoritesGroupId == ""):
      GETFAVORITEGROUP()

    if (username == "" or password == ""):
      xbmcgui.Dialog().ok(LB_ERROR, LB_NOLOGIN)
      xbmcaddon.Addon(id='plugin.video.hbogoeu').openSettings()
      xbmc.executebuiltin("Action(Back)")
      return

    headers = {
        'Origin': API_HOST_GATEWAY,
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'hr,en-US;q=0.9,en;q=0.8',
        'User-Agent': UA,
        'GO-Token': '',
        'Accept': 'application/json',
        'GO-SessionId': '',
        'Referer': API_HOST_GATEWAY_REFERER,
        'Connection': 'keep-alive',
        'GO-CustomerId': '00000000-0000-0000-0000-000000000000',
        'Content-Type': 'application/json',
    }

    if IS_WEB:
        url = API_URL_AUTH_WEBBASIC
    else:
        url = API_URL_AUTH_OPERATOR

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
            "Individualization": individualization,
            "IsDeleted": False,
            "LastUsed": "",
            "Modell": "62",
            "Name": "",
            "OSName": "Ubuntu",
            "OSVersion": "undefined",
            "Platform": API_PLATFORM,
            "SWVersion": "2.4.2.4025.240",
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
        "Language": LANGUAGE_CODE,
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
    r = requests.post(url, headers=headers, data=data)
    jsonrspl = json.loads(r.text)

    try:
        if jsonrspl['ErrorMessage']:
            xbmcgui.Dialog().ok(LB_ERROR, jsonrspl['ErrorMessage'])
            xbmc.executebuiltin("Action(Back)")
            return
    except:
        pass

    customerId = jsonrspl['Customer']['CurrentDevice']['Id']
    individualization = jsonrspl['Customer']['CurrentDevice']['Individualization']

    sessionId = jsonrspl['SessionId']
    if sessionId == '00000000-0000-0000-0000-000000000000':
        xbmcgui.Dialog().ok(LB_ERROR, LB_LOGIN_ERROR)
        xbmc.executebuiltin("Action(Back)")
        return
    else:
        goToken = jsonrspl['Token']
        GOcustomerId = jsonrspl['Customer']['Id']

        loggedin_headers['GO-SessionId'] = str(sessionId)
        loggedin_headers['GO-Token'] = str(goToken)
        loggedin_headers['GO-CustomerId'] = str(GOcustomerId)


# kategoria
def CATEGORIES():
    global FavoritesGroupId

    addDir(LB_SEARCH, 'search', '', 4, '')

    if (FavoritesGroupId == ""):
        GETFAVORITEGROUP()

    if (FavoritesGroupId != ""):
        addDir(LB_MYPLAYLIST, API_URL_CUSTOMER_GROUP + FavoritesGroupId + '/-/-/-/1000/-/-/false', '', 1,
               md + 'FavoritesFolder.png')

    req = urllib2.Request(API_URL_GROUPS, None, loggedin_headers)
    opener = urllib2.build_opener()
    f = opener.open(req)
    jsonrsp = json.loads(f.read())

    try:
        if jsonrsp['ErrorMessage']:
            xbmcgui.Dialog().ok(LB_ERROR, jsonrsp['ErrorMessage'])
    except:
        pass

    for cat in range(0, len(jsonrsp['Items'])):
        addDir(jsonrsp['Items'][cat]['Name'].encode('utf-8', 'ignore'),
               jsonrsp['Items'][cat]['ObjectUrl'].replace('/0/{sort}/{pageIndex}/{pageSize}/0/0', '/0/0/1/1024/0/0'),
               '', 1, md + 'DefaultFolder.png')


# lista
def LIST(url):
    global sessionId
    global loggedin_headers

    if sessionId == '00000000-0000-0000-0000-000000000000':
        LOGIN()

    req = urllib2.Request(url, None, loggedin_headers)
    opener = urllib2.build_opener()
    f = opener.open(req)
    jsonrsp = json.loads(f.read())

    try:
        if jsonrsp['ErrorMessage']:
            xbmcgui.Dialog().ok(LB_ERROR, jsonrsp['ErrorMessage'])
    except:
        pass
    # If there is a subcategory / genres
    if len(jsonrsp['Container']) > 1:
        for Container in range(0, len(jsonrsp['Container'])):
            addDir(jsonrsp['Container'][Container]['Name'].encode('utf-8', 'ignore'),
                   jsonrsp['Container'][Container]['ObjectUrl'], '', 1, md + 'DefaultFolder.png')
    else:
        for titles in range(0, len(jsonrsp['Container'][0]['Contents']['Items'])):
            if jsonrsp['Container'][0]['Contents']['Items'][titles][
                'ContentType'] == 1:  # 1=MOVIE/EXTRAS, 2=SERIES(serial), 3=SERIES(episode)
                plot = jsonrsp['Container'][0]['Contents']['Items'][titles]['Abstract'].encode('utf-8', 'ignore')
                if 'AvailabilityTo' in jsonrsp['Container'][0]['Contents']['Items'][titles]:
                    if jsonrsp['Container'][0]['Contents']['Items'][titles]['AvailabilityTo'] is not None:
                        plot = plot + ' ' + LB_FILM_UNTILL + ' ' + jsonrsp['Container'][0]['Contents']['Items'][titles][
                            'AvailabilityTo'].encode('utf-8', 'ignore')
                addLink(jsonrsp['Container'][0]['Contents']['Items'][titles]['ObjectUrl'], plot,
                        jsonrsp['Container'][0]['Contents']['Items'][titles]['AgeRating'],
                        jsonrsp['Container'][0]['Contents']['Items'][titles]['ImdbRate'],
                        jsonrsp['Container'][0]['Contents']['Items'][titles]['BackgroundUrl'],
                        [jsonrsp['Container'][0]['Contents']['Items'][titles]['Cast'].split(', ')][0],
                        jsonrsp['Container'][0]['Contents']['Items'][titles]['Director'],
                        jsonrsp['Container'][0]['Contents']['Items'][titles]['Writer'],
                        jsonrsp['Container'][0]['Contents']['Items'][titles]['Duration'],
                        jsonrsp['Container'][0]['Contents']['Items'][titles]['Genre'],
                        jsonrsp['Container'][0]['Contents']['Items'][titles]['Name'].encode('utf-8', 'ignore'),
                        jsonrsp['Container'][0]['Contents']['Items'][titles]['OriginalName'],
                        jsonrsp['Container'][0]['Contents']['Items'][titles]['ProductionYear'], 5)
                xbmc.log("GO: FILM: DUMP: " + jsonrsp['Container'][0]['Contents']['Items'][titles]['ObjectUrl'])

            elif jsonrsp['Container'][0]['Contents']['Items'][titles]['ContentType'] == 3:
                plot = jsonrsp['Container'][0]['Contents']['Items'][titles]['Abstract'].encode('utf-8', 'ignore')
                if jsonrsp['Container'][0]['Contents']['Items'][titles]['AvailabilityTo'] is not None:
                    plot = plot + ' ' + LB_EPIZODE_UNTILL + ' ' + jsonrsp['Container'][0]['Contents']['Items'][titles][
                        'AvailabilityTo'].encode('utf-8', 'ignore')
                addLink(jsonrsp['Container'][0]['Contents']['Items'][titles]['ObjectUrl'], plot,
                        jsonrsp['Container'][0]['Contents']['Items'][titles]['AgeRating'],
                        jsonrsp['Container'][0]['Contents']['Items'][titles]['ImdbRate'],
                        jsonrsp['Container'][0]['Contents']['Items'][titles]['BackgroundUrl'],
                        [jsonrsp['Container'][0]['Contents']['Items'][titles]['Cast'].split(', ')][0],
                        jsonrsp['Container'][0]['Contents']['Items'][titles]['Director'],
                        jsonrsp['Container'][0]['Contents']['Items'][titles]['Writer'],
                        jsonrsp['Container'][0]['Contents']['Items'][titles]['Duration'],
                        jsonrsp['Container'][0]['Contents']['Items'][titles]['Genre'],
                        jsonrsp['Container'][0]['Contents']['Items'][titles]['SeriesName'].encode('utf-8',
                                                                                                  'ignore') + ' - ' + str(
                            jsonrsp['Container'][0]['Contents']['Items'][titles][
                                'SeasonIndex']) + '. ' + LB_SEASON + ' ' + str(
                            jsonrsp['Container'][0]['Contents']['Items'][titles]['Index']) + '. ' + LB_EPISODE,
                        jsonrsp['Container'][0]['Contents']['Items'][titles]['OriginalName'],
                        jsonrsp['Container'][0]['Contents']['Items'][titles]['ProductionYear'], 5)
            else:
                addDir(jsonrsp['Container'][0]['Contents']['Items'][titles]['Name'].encode('utf-8', 'ignore'),
                       jsonrsp['Container'][0]['Contents']['Items'][titles]['ObjectUrl'],
                       jsonrsp['Container'][0]['Contents']['Items'][titles]['Abstract'].encode('utf-8', 'ignore'), 2,
                       jsonrsp['Container'][0]['Contents']['Items'][titles]['BackgroundUrl'])


# SEZONA OK
def SEASON(url):
    req = urllib2.Request(url, None, loggedin_headers)
    opener = urllib2.build_opener()
    f = opener.open(req)
    jsonrsp = json.loads(f.read())

    try:
        if jsonrsp['ErrorMessage']:
            xbmcgui.Dialog().ok(LB_ERROR, jsonrsp['ErrorMessage'])
    except:
        pass
    for season in range(0, len(jsonrsp['Parent']['ChildContents']['Items'])):
        addDir(jsonrsp['Parent']['ChildContents']['Items'][season]['Name'].encode('utf-8', 'ignore'),
               jsonrsp['Parent']['ChildContents']['Items'][season]['ObjectUrl'],
               jsonrsp['Parent']['ChildContents']['Items'][season]['Abstract'].encode('utf-8', 'ignore'), 3,
               jsonrsp['Parent']['ChildContents']['Items'][season]['BackgroundUrl'])


# epizodok
def EPISODE(url):
    req = urllib2.Request(url, None, loggedin_headers)
    opener = urllib2.build_opener()
    f = opener.open(req)
    jsonrsp = json.loads(f.read())

    try:
        if jsonrsp['ErrorMessage']:
            xbmcgui.Dialog().ok(LB_ERROR, jsonrsp['ErrorMessage'])
    except:
        pass

    for episode in range(0, len(jsonrsp['ChildContents']['Items'])):
        # addLink(ou,plot,ar,imdb,bu,cast,director,writer,duration,genre,name,on,py,mode)
        plot = jsonrsp['ChildContents']['Items'][episode]['Abstract'].encode('utf-8', 'ignore')
        if 'AvailabilityTo' in jsonrsp['ChildContents']['Items'][episode]:
            if jsonrsp['ChildContents']['Items'][episode]['AvailabilityTo'] is not None:
                plot = plot + ' ' + LB_EPIZODE_UNTILL + ' ' + jsonrsp['ChildContents']['Items'][episode][
                    'AvailabilityTo'].encode('utf-8', 'ignore')
        addLink(jsonrsp['ChildContents']['Items'][episode]['ObjectUrl'], plot,
                jsonrsp['ChildContents']['Items'][episode]['AgeRating'],
                jsonrsp['ChildContents']['Items'][episode]['ImdbRate'],
                jsonrsp['ChildContents']['Items'][episode]['BackgroundUrl'],
                [jsonrsp['ChildContents']['Items'][episode]['Cast'].split(', ')][0],
                jsonrsp['ChildContents']['Items'][episode]['Director'],
                jsonrsp['ChildContents']['Items'][episode]['Writer'],
                jsonrsp['ChildContents']['Items'][episode]['Duration'],
                jsonrsp['ChildContents']['Items'][episode]['Genre'],
                jsonrsp['ChildContents']['Items'][episode]['SeriesName'].encode('utf-8', 'ignore') + ' - ' + str(
                    jsonrsp['ChildContents']['Items'][episode]['SeasonIndex']) + '. SEZONA ' +
                jsonrsp['ChildContents']['Items'][episode]['Name'].encode('utf-8', 'ignore'),
                jsonrsp['ChildContents']['Items'][episode]['OriginalName'],
                jsonrsp['ChildContents']['Items'][episode]['ProductionYear'], 5)


# lejatszas
def PLAY(url):
    global goToken
    global individualization
    global customerId
    global GOcustomerId
    global sessionId
    global loggedin_headers

    if sessionId == '00000000-0000-0000-0000-000000000000':
        LOGIN()

    purchase_payload = '<Purchase xmlns="go:v5:interop"><AllowHighResolution>true</AllowHighResolution><ContentId>' + cid + '</ContentId><CustomerId>' + GOcustomerId + '</CustomerId><Individualization>' + individualization + '</Individualization><OperatorId>' + op_id + '</OperatorId><ClientInfo></ClientInfo><IsFree>false</IsFree><UseInteractivity>false</UseInteractivity></Purchase>'

    purchase_headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding': '',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'GO-CustomerId': str(GOcustomerId),
        'GO-requiredPlatform': 'CHBR',
        'GO-SessionId': str(sessionId),
        'GO-swVersion': '4.7.4',
        'GO-Token': str(goToken),
        'Host': API_HOST,
        'Referer': API_HOST_REFERER,
        'Origin': API_HOST_ORIGIN,
        'User-Agent': UA
    }

    req = urllib2.Request(API_URL_PURCHASE, purchase_payload, purchase_headers)
    opener = urllib2.build_opener()
    f = opener.open(req)
    jsonrspp = json.loads(f.read())
    xbmc.log(str(jsonrspp))

    try:
        if jsonrspp['ErrorMessage']:
            xbmcgui.Dialog().ok(LB_ERROR, jsonrspp['ErrorMessage'])
    except:
        pass

    MediaUrl = jsonrspp['Purchase']['MediaUrl'] + "/Manifest"
    PlayerSessionId = jsonrspp['Purchase']['PlayerSessionId']
    x_dt_auth_token = jsonrspp['Purchase']['AuthToken']
    dt_custom_data = base64.b64encode(
        "{\"userId\":\"" + GOcustomerId + "\",\"sessionId\":\"" + PlayerSessionId + "\",\"merchant\":\"hboeurope\"}")

    li = xbmcgui.ListItem(iconImage=thumbnail, thumbnailImage=thumbnail, path=MediaUrl)
    license_server = LICENSE_SERVER
    license_headers = 'dt-custom-data=' + dt_custom_data + '&x-dt-auth-token=' + x_dt_auth_token + '&Origin=' + API_HOST_ORIGIN + '&Content-Type='
    license_key = license_server + '|' + license_headers + '|R{SSM}|JBlicense'

    protocol = 'ism'
    drm = 'com.widevine.alpha'
    is_helper = inputstreamhelper.Helper(protocol, drm=drm)
    is_helper.check_inputstream()
    li.setProperty('inputstreamaddon', 'inputstream.adaptive')
    li.setProperty('inputstream.adaptive.manifest_type', protocol)
    li.setProperty('inputstream.adaptive.license_type', drm)
    li.setProperty('inputstream.adaptive.license_data', 'ZmtqM2xqYVNkZmFsa3Izag==')
    li.setProperty('inputstream.adaptive.license_key', license_key)

    xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)


def SEARCH():
    keyb = xbmc.Keyboard(search_string, LB_SEARCH_DESC)
    keyb.doModal()
    searchText = ''
    if (keyb.isConfirmed()):
        searchText = urllib.quote_plus(keyb.getText())
        if searchText == "":
            addDir(LB_SEARCH_NORES, '', '', '', md + 'DefaultFolderBack.png')
        else:
            __settings__.setSetting('lastsearch', searchText)

            req = urllib2.Request(
                API_URL_SEARCH + searchText.decode('utf-8', 'ignore').encode('utf-8', 'ignore') + '/0', None,
                loggedin_headers)
            opener = urllib2.build_opener()
            f = opener.open(req)
            jsonrsp = json.loads(f.read())
            xbmc.log(str(jsonrsp))

            try:
                if jsonrsp['ErrorMessage']:
                    xbmcgui.Dialog().ok(LB_ERROR, jsonrsp['ErrorMessage'])
            except:
                pass

            br = 0
            for index in range(0, len(jsonrsp['Container'][0]['Contents']['Items'])):
                if (jsonrsp['Container'][0]['Contents']['Items'][index]['ContentType'] == 1 or
                        jsonrsp['Container'][0]['Contents']['Items'][index][
                            'ContentType'] == 7):  # 1,7=MOVIE/EXTRAS, 2=SERIES(serial), 3=SERIES(episode)
                    # addLink(ou,plot,ar,imdb,bu,cast,director,writer,duration,genre,name,on,py,mode)
                    addLink(jsonrsp['Container'][0]['Contents']['Items'][index]['ObjectUrl'],
                            jsonrsp['Container'][0]['Contents']['Items'][index]['Abstract'].encode('utf-8', 'ignore'),
                            jsonrsp['Container'][0]['Contents']['Items'][index]['AgeRating'],
                            jsonrsp['Container'][0]['Contents']['Items'][index]['ImdbRate'],
                            jsonrsp['Container'][0]['Contents']['Items'][index]['BackgroundUrl'],
                            [jsonrsp['Container'][0]['Contents']['Items'][index]['Cast'].split(', ')][0],
                            jsonrsp['Container'][0]['Contents']['Items'][index]['Director'],
                            jsonrsp['Container'][0]['Contents']['Items'][index]['Writer'],
                            jsonrsp['Container'][0]['Contents']['Items'][index]['Duration'],
                            jsonrsp['Container'][0]['Contents']['Items'][index]['Genre'],
                            jsonrsp['Container'][0]['Contents']['Items'][index]['Name'].encode('utf-8', 'ignore'),
                            jsonrsp['Container'][0]['Contents']['Items'][index]['OriginalName'],
                            jsonrsp['Container'][0]['Contents']['Items'][index]['ProductionYear'], 5)
                elif jsonrsp['Container'][0]['Contents']['Items'][index]['ContentType'] == 3:
                    # addLink(ou,plot,ar,imdb,bu,cast,director,writer,duration,genre,name,on,py,mode)
                    addLink(jsonrsp['Container'][0]['Contents']['Items'][index]['ObjectUrl'],
                            jsonrsp['Container'][0]['Contents']['Items'][index]['Abstract'].encode('utf-8', 'ignore'),
                            jsonrsp['Container'][0]['Contents']['Items'][index]['AgeRating'],
                            jsonrsp['Container'][0]['Contents']['Items'][index]['ImdbRate'],
                            jsonrsp['Container'][0]['Contents']['Items'][index]['BackgroundUrl'],
                            [jsonrsp['Container'][0]['Contents']['Items'][index]['Cast'].split(', ')][0],
                            jsonrsp['Container'][0]['Contents']['Items'][index]['Director'],
                            jsonrsp['Container'][0]['Contents']['Items'][index]['Writer'],
                            jsonrsp['Container'][0]['Contents']['Items'][index]['Duration'],
                            jsonrsp['Container'][0]['Contents']['Items'][index]['Genre'],
                            jsonrsp['Container'][0]['Contents']['Items'][index]['SeriesName'].encode('utf-8',
                                                                                                     'ignore') + ' ' +
                            jsonrsp['Container'][0]['Contents']['Items'][index]['Name'].encode('utf-8', 'ignore'),
                            jsonrsp['Container'][0]['Contents']['Items'][index]['OriginalName'],
                            jsonrsp['Container'][0]['Contents']['Items'][index]['ProductionYear'], 5)
                else:
                    addDir(jsonrsp['Container'][0]['Contents']['Items'][index]['Name'].encode('utf-8', 'ignore'),
                           jsonrsp['Container'][0]['Contents']['Items'][index]['ObjectUrl'],
                           jsonrsp['Container'][0]['Contents']['Items'][index]['Abstract'].encode('utf-8', 'ignore'), 2,
                           jsonrsp['Container'][0]['Contents']['Items'][index]['BackgroundUrl'])
                br = br + 1
            if br == 0:
                addDir(LB_SEARCH_NORES, '', '', '', md + 'DefaultFolderBack.png')


def addLink(ou, plot, ar, imdb, bu, cast, director, writer, duration, genre, name, on, py, mode):
    cid = ou.rsplit('/', 2)[1]
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(
        name) + "&cid=" + cid + "&thumbnail=" + bu
    ok = True
    liz = xbmcgui.ListItem(name, iconImage=bu, thumbnailImage=bu)
    liz.setArt({'thumb': bu, 'poster': bu, 'banner': bu, 'fanart': bu})
    liz.setInfo(type="Video",
                infoLabels={"plot": plot, "mpaa": str(ar) + '+', "rating": imdb, "cast": cast, "director": director,
                            "writer": writer, "duration": duration, "genre": genre, "title": name, "originaltitle": on,
                            "year": py})
    liz.addStreamInfo('video', {'width': 1280, 'height': 720})
    liz.addStreamInfo('video', {'aspect': 1.78, 'codec': 'h264'})
    liz.addStreamInfo('audio', {'codec': 'aac', 'channels': 2})
    liz.setProperty("IsPlayable", "true")
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=False)
    return ok


def addDir(name, url, plot, mode, iconimage):
    u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
    ok = True
    liz = xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
    liz.setInfo(type="Video", infoLabels={"Title": name, "Plot": plot})
    ok = xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]), url=u, listitem=liz, isFolder=True)
    return ok


def get_params():
    param = []
    paramstring = sys.argv[2]
    if len(paramstring) >= 2:
        params = sys.argv[2]
        cleanedparams = params.replace('?', '')
        if (params[len(params) - 1] == '/'):
            params = params[0:len(params) - 2]
        pairsofparams = cleanedparams.split('&')
        param = {}
        for i in range(len(pairsofparams)):
            splitparams = {}
            splitparams = pairsofparams[i].split('=')
            if (len(splitparams)) == 2:
                param[splitparams[0]] = splitparams[1]
    return param


params = get_params()
url = None
name = None
iconimage = None
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
    cid = str(params["cid"])
except:
    pass

if mode == None or url == None or len(url) < 1:
    CATEGORIES()

elif mode == 1:
    LIST(url)

elif mode == 2:
    SEASON(url)

elif mode == 3:
    EPISODE(url)

elif mode == 4:
    SEARCH()

elif mode == 5:
    PLAY(url)

elif mode == 6:
    SILENTREGISTER()

elif mode == 7:
    LOGIN()

xbmcplugin.endOfDirectory(int(sys.argv[1]))
