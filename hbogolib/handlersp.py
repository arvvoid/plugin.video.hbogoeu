from hbogolib.handler import HbogoHandler
from hbogolib.handlereu import HbogoHandler_eu

import sys
import base64
import random
import math
import urllib
import copy
from lxml import etree as ET

import xbmcgui
import xbmcplugin
import inputstreamhelper

class HbogoHandler_sp(HbogoHandler):

    def __init__(self, handle, base_url):
        HbogoHandler.__init__(self, handle, base_url)

        self.LICENSE_SERVER = ""

        self.API_CLIENT_VERSION = '3.8.3'
        self.API_DEVICE_ID = ''
        self.API_DEVICE_TOKEN = ''
        self.API_IDENTITY_GUID = ''
        self.API_ACCOUNT_GUID = ''

        self.API_HOST = 'api-hboe.hbo.clearleap.com'
        self.API_HOST_GATEWAY = 'https://es.hboespana.com'
        self.API_HOST_GATEWAY_REFERER = self.API_HOST_GATEWAY + '/sign-in'

        self.API_URL_BROWSE = 'https://api-hboe.hbo.clearleap.com/cloffice/client/web/browse/'
        self.API_URL_AUTH_WEBBASIC = 'https://api-hboe.hbo.clearleap.com/cloffice/client/device/login'

        if len(self.getCredential('username')) == 0:
            self.setup()
        else:
            self.init_api()

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

    def generate_device_id(self):
        def rand_hex():
            return hex(random.getrandbits(16))[2:].zfill(4)

        return rand_hex() + rand_hex() + "-" + rand_hex() + "-" + rand_hex() + "-" + rand_hex() + "-" + rand_hex() + rand_hex() + rand_hex()

    def chk_login(self):
        return self.API_DEVICE_TOKEN != ''

    def login(self):
        username = self.getCredential('username')
        password = self.getCredential('password')

        headers = {
            'Host': self.API_HOST,
            'User-Agent': self.UA,
            'Accept': '*/*',
            'Accept-Language': self.ACCEPT_LANGUAGE,
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': self.API_HOST_GATEWAY_REFERER,
            'Content-Type': 'application/xml',
            'Authorization': 'Basic ' + base64.b64encode(username + ':' + base64.b64encode(password)),
            'Origin': self.API_HOST_GATEWAY,
            'Connection': 'keep-alive',
        }

        self.API_DEVICE_ID = self.generate_device_id()

        data = '<device><type>web</type><deviceId>' + self.API_DEVICE_ID + '</deviceId></device>'

        response = self.send_login_hbogo(self.API_URL_AUTH_WEBBASIC, headers, data, 'xml')


        if response.xpath('status')[0].text == 'Success':
            self.API_DEVICE_TOKEN = response.xpath('token')[0].text
            self.API_IDENTITY_GUID = response.xpath('identityGuid')[0].text
            self.API_ACCOUNT_GUID = response.xpath('accountGuid')[0].text
            self.init_api()
            return True
        else:
            return False


    def setup(self):
        self.init_api()
        if self.inputCredentials():
            return True
        else:
            self.del_setup()
            xbmcgui.Dialog().ok(self.LB_ERROR, self.language(30444).encode('utf-8'))
            sys.exit()
            return False

    def init_api(self):
        self.loggedin_headers = {
            'Host': self.API_HOST,
            'User-Agent': self.UA,
            'Accept': '*/*',
            'Accept-Language': self.ACCEPT_LANGUAGE,
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': self.API_HOST_GATEWAY_REFERER,
            'X-Client-Name': 'web',
            'X-Client-Version': self.API_CLIENT_VERSION,
            'X-Clearleap-DeviceId': self.API_DEVICE_ID,
            'X-Clearleap-DeviceToken': self.API_DEVICE_TOKEN,
            'Origin': self.API_HOST_GATEWAY,
            'Connection': 'keep-alive',
        }

    def categories(self):
        if not self.chk_login():
            self.login()

        browse_xml = self.get_from_hbogo(self.API_URL_BROWSE, response_format='xml')

        home = None
        series = None
        movies = None
        kids = None

        for item in browse_xml.xpath('.//item'):
            if item.xpath('category')[0].text == 'Home':
                home = item
            elif item.xpath('category')[0].text == 'Series':
                series = item
            elif item.xpath('category')[0].text == 'Movies':
                movies = item
            elif item.xpath('category')[0].text == 'Kids':
                kids = item
            else:
                pass

        if series != None:
            self.addCat(self.language(30716).encode('utf-8'), series.xpath('link')[0].text, self.md + 'tv.png', 1)
        else:
            self.log("No Series Category found")
        
        if movies != None:
            self.addCat(self.language(30717).encode('utf-8'), movies.xpath('link')[0].text, self.md + 'movie.png', 1)
        else:
            self.log("No Movies Category found")

        if kids != None:
            self.addCat(self.language(30729).encode('utf-8'), kids.xpath('link')[0].text, self.md + 'kids.png', 1)
        else:
            self.log("No Kids Category found")

        if home != None:
            self.list(home.xpath('link')[0].text, True)
        else:
            self.log("No Home Category found")


        xbmcplugin.addSortMethod(
            handle=self.handle,
            sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)
        xbmcplugin.endOfDirectory(self.handle)

    def get_thumbnail_url(self, item):
        thumbnail_url = item.xpath('media:thumbnail', namespaces=item.nsmap)
        return thumbnail_url[0].get('url') if thumbnail_url else '' 

    def list(self, url, simple=False):
        if not self.chk_login():
            self.login()
        self.log("List: " + str(url))

        if not self.chk_login():
            self.login()

        response = self.get_from_hbogo(url, 'xml')

        for item in response.xpath('.//item'):
            item_link = item.xpath('link')[0].text

            if len(item_link) > 0:
                item_type = item.xpath('clearleap:itemType', namespaces=response.nsmap)[0].text.encode('utf-8')
                if item_type == 'LEAF':
                    self.addDir(item)
                elif item_type == 'CATEGORY':
                    self.addCat(item.xpath('title')[0].text.encode('utf-8'), item_link, self.get_thumbnail_url(item), 1)
                elif item_type == 'media':
                    self.addLink(item, 5)
                else:
                    self.log('Unknown item type: ' + item_type)
    
        if simple == False:
            xbmcplugin.addSortMethod(handle=self.handle, sortMethod=xbmcplugin.SORT_METHOD_UNSORTED)
            xbmcplugin.addSortMethod(handle=self.handle, sortMethod=xbmcplugin.SORT_METHOD_LABEL)
            xbmcplugin.addSortMethod(handle=self.handle, sortMethod=xbmcplugin.SORT_METHOD_TITLE)
            xbmcplugin.addSortMethod(handle=self.handle, sortMethod=xbmcplugin.SORT_METHOD_VIDEO_YEAR)
            xbmcplugin.addSortMethod(handle=self.handle, sortMethod=xbmcplugin.SORT_METHOD_GENRE)
            xbmcplugin.addSortMethod(handle=self.handle, sortMethod=xbmcplugin.SORT_METHOD_LASTPLAYED)
            xbmcplugin.setContent(self.handle, self.use_content_type)
            xbmcplugin.endOfDirectory(self.handle)
    
    def play(self, url, content_id):
        self.log("Play: " + str(url))

        if not self.chk_login():
            self.login()
        
        if not self.chk_login():
            self.log("NOT LOGGED IN, ABORTING PLAY")
            xbmcgui.Dialog().ok(self.LB_LOGIN_ERROR, self.language(30103).encode('utf-8'))
            self.logout()
            return

        media_item = self.get_from_hbogo(url, 'xml')

        mpd_pre_url = media_item.xpath('.//media:content[@profile="HBO-DASH-WIDEVINE"]', namespaces=media_item.nsmap)[0].get('url') + '&responseType=xml'

        mpd_url = self.get_from_hbogo(mpd_pre_url, 'xml').xpath('.//url')[0].text

        media_guid = media_item.xpath('.//guid')[0].text

        license_headers = 'X-Clearleap-AssetID=' + media_guid + '&X-Clearleap-DeviceId=' + self.API_DEVICE_ID + \
            '&X-Clearleap-DeviceToken=' + self.API_DEVICE_TOKEN + '&Content-Type='
    
        license_url = 'https://api-hboe.hbo.clearleap.com/cloffice/drm/wv/' + media_guid + '|' + license_headers + '|R{SSM}|'

        li = xbmcgui.ListItem(path=mpd_url)
        protocol = 'mpd'
        drm = 'com.widevine.alpha'
        is_helper = inputstreamhelper.Helper(protocol, drm=drm)
        is_helper.check_inputstream()
        li.setProperty('inputstreamaddon', 'inputstream.adaptive')
        li.setProperty('inputstream.adaptive.license_type', drm)
        li.setProperty('inputstream.adaptive.manifest_type', protocol)
        li.setProperty('inputstream.adaptive.license_key', license_url)

        li.setMimeType('application/dash+xml')
        li.setContentLookup(False)

        self.log("Play url: " + str(li))
        xbmcplugin.setResolvedUrl(self.handle, True, listitem=li)

    def addLink(self, title, mode):
        self.log("Adding Link: " + str(title) + " MODE: " + str(mode))

        name = title.xpath('title')[0].text.encode('utf-8')
        media_type = "episode"

        u = self.base_url + "?url=" + urllib.quote_plus(title.xpath('link')[0].text) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)

        liz = xbmcgui.ListItem(name)
        liz.setInfo(type="Video",
                    infoLabels={"mediatype": media_type,})
        liz.addStreamInfo('video', {'width': 1920, 'height': 1080})
        liz.addStreamInfo('video', {'aspect': 1.78, 'codec': 'h264'})
        liz.addStreamInfo('audio', {'codec': 'aac', 'channels': 2})
        liz.setProperty("IsPlayable", "true")
        xbmcplugin.addDirectoryItem(handle=self.handle, url=u, listitem=liz, isFolder=False)


    def addDir(self, item):
        showtitle = item.xpath('clearleap:shortTitle', namespaces=item.nsmap)
        showtitle = showtitle[0].text.encode('utf-8') if showtitle else ''

        self.addCat(item.xpath('title')[0].text.encode('utf-8'), item.xpath('link')[0].text, self.get_thumbnail_url(item), 1)

    def addCat(self, name, url, icon, mode):
        self.log("Adding Cat: " + str(name) + "," + str(url) + "," + str(icon) + " MODE: " + str(mode))
        u = self.base_url + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name)
        liz = xbmcgui.ListItem(name, iconImage=icon, thumbnailImage=icon)
        liz.setArt({'fanart': self.resources + "fanart.jpg"})
        liz.setInfo(type="Video", infoLabels={"Title": name})
        liz.setProperty('isPlayable', "false")
        xbmcplugin.addDirectoryItem(handle=self.handle, url=u, listitem=liz, isFolder=True)