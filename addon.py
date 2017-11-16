# -*- coding: utf-8 -*-
#mudlok
import re
import sys
import os
import urllib
import urllib2
import requests
import json
import xbmc
import xbmcgui
import xbmcplugin
import xbmcaddon
import xbmcvfs
import base64
import time
import random


__addon_id__= 'plugin.video.hbogohu'
__Addon = xbmcaddon.Addon(__addon_id__)
__settings__ = xbmcaddon.Addon(id='plugin.video.hbogohu')

UA = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.79 Safari/537.36'
MUA = 'Dalvik/2.1.0 (Linux; U; Android 8.0.0; Nexus 5X Build/OPP3.170518.006)'

se = __settings__.getSetting('se')
language = __settings__.getSetting('language')
if language == '0':
	lang = 'Hungarian'
	Code = 'HUN'
	srtsubs_path = xbmc.translatePath('special://temp/hbogo.Hungarian.Forced.srt')
elif language == '1':
	lang = 'Hungarian'
	Code = 'HUN'
	srtsubs_path = xbmc.translatePath('special://temp/hbogo.Hungarian.Forced.srt')
elif language == '2':
	lang = 'English'
	Code = 'ENG'
	srtsubs_path = xbmc.translatePath('special://temp/hbogo.English.Forced.srt')
	

md = xbmc.translatePath(__Addon.getAddonInfo('path') + "/resources/media/")
search_string = urllib.unquote_plus(__settings__.getSetting('lastsearch'))

operator = __settings__.getSetting('operator')
op_ids = [
'00000000-0000-0000-0000-000000000000', # Anonymous NoAuthenticated
'15276cb7-7f53-432a-8ed5-a32038614bbf', # HBO GO 
'48f48c5b-e9e4-4fca-833b-2fa26fb1ad22', # UPC Dire

]
op_id = op_ids[int(operator)];



username = __settings__.getSetting('username')
password = __settings__.getSetting('password')

individualization = ""
goToken = ""
customerId = ""
GOcustomerId = ""
sessionId = '00000000-0000-0000-0000-000000000000'

loggedin_headers = {
	'User-Agent': UA,
	'Accept': '*/*',
	'Accept-Language': 'en-US,en;q=0.5',
	'Referer': 'https://www.hbogo.hu/',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'Origin': 'https://www.hbogo.hu',
	'X-Requested-With': 'XMLHttpRequest',
	'GO-Language': 'HUN',
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





def SILENTREGISTER():
	global goToken
	global individualization
	global customerId
	global sessionId

	req = urllib2.Request('https://hu.hbogo.eu/services/settings/silentregister.aspx', None, loggedin_headers)

	opener = urllib2.build_opener()
	f = opener.open(req)
	jsonrsp = json.loads(f.read())

	if jsonrsp['Data']['ErrorMessage']:
		xbmcgui.Dialog().ok('Error', jsonrsp['Data']['ErrorMessage'])

	indiv = jsonrsp['Data']['Customer']['CurrentDevice']['Individualization']
	custid = jsonrsp['Data']['Customer']['CurrentDevice']['Id'];
	storeIndiv(indiv, custid)

	sessionId= jsonrsp['Data']['SessionId']
	return jsonrsp






def LOGIN():
	global sessionId
	global goToken
	global customerId
	global GOcustomerId
	global individualization
	global loggedin_headers


	customerId = __settings__.getSetting('customerId')
	individualization = __settings__.getSetting('individualization')

	if (individualization == "" or customerId == ""):
		jsonrsp = SILENTREGISTER()

	if (username=="" or password==""):
		xbmcgui.Dialog().ok('Hiba','Nincs beallitva megfelelo felhasznalo.')
		xbmcaddon.Addon(id='plugin.video.hbogohu').openSettings("Акаунт")
		xbmc.executebuiltin("Container.Refresh")
		LOGIN()

	headers = {
		'Origin': 'https://gateway.hbogo.eu',
		'Accept-Encoding': 'gzip, deflate, br',
		'Accept-Language': 'hu,en-US;q=0.9,en;q=0.8',
		'User-Agent': UA,
		'GO-Token': '',
		'Accept': 'application/json',
		'GO-SessionId': '',
		'Referer': 'https://gateway.hbogo.eu/signin/form',
		'Connection': 'keep-alive',
		'GO-CustomerId': '00000000-0000-0000-0000-000000000000',
		'Content-Type': 'application/json',
	}

	data = '{"Action":"L","AppLanguage":null,"ActivationCode":null,"AllowedContents":[],"AudioLanguage":null,"AutoPlayNext":false,"BirthYear":0,"CurrentDevice":{"AppLanguage":"","AutoPlayNext":false,"Brand":"Chromium","CreatedDate":"","DeletedDate":"","Id":"00000000-0000-0000-0000-000000000000","Individualization":"'+individualization+'","IsDeleted":false,"LastUsed":"","Modell":"62","Name":"","OSName":"Ubuntu","OSVersion":"undefined","Platform":"COMP","SWVersion":"2.4.2.4025.240","SubtitleSize":""},"CustomerCode":"","DebugMode":false,"DefaultSubtitleLanguage":null,"EmailAddress":"'+username+'","FirstName":"","Gender":0,"Id":"00000000-0000-0000-0000-000000000000","IsAnonymus":true,"IsPromo":false,"Language":"HUN","LastName":"","Nick":"","NotificationChanges":0,"OperatorId":"'+op_id+'","OperatorName":"","OperatorToken":"","ParentalControl":{"Active":false,"Password":"","Rating":0,"ReferenceId":"00000000-0000-0000-0000-000000000000"},"Password":"'+password+'","PromoCode":"","ReferenceId":"00000000-0000-0000-0000-000000000000","SecondaryEmailAddress":"","SecondarySpecificData":null,"ServiceCode":"","SubscribeForNewsletter":false,"SubscState":null,"SubtitleSize":"","TVPinCode":"","ZipCode":""}'
	r = requests.post('https://api.ugw.hbogo.eu/v3.0/Authentication/HUN/JSON/HUN/COMP', headers=headers, data=data)


	jsonrspl = json.loads(r.text)

	try:
		if jsonrspl['ErrorMessage']:
			xbmcgui.Dialog().ok('Login Hiba!', jsonrspl['ErrorMessage'])
	except:
		pass

	customerId = jsonrspl['Customer']['CurrentDevice']['Id']
	individualization = jsonrspl['Customer']['CurrentDevice']['Individualization']

	sessionId = jsonrspl['SessionId']
	if sessionId == '00000000-0000-0000-0000-000000000000':
		xbmcgui.Dialog().ok('Login Hiba!','Ellenőrizd a belépési adatokat!')
		xbmcaddon.Addon(id='plugin.video.hbogohu').openSettings("Акаунт")
		xbmc.executebuiltin("Action(Back)")
	else:
		xbmc.executebuiltin('Notification(%s, %s, %d, %s)'%(username,'Belépve!', 4000, md+'DefaultUser.png'))

		goToken = jsonrspl['Token']
		GOcustomerId = jsonrspl['Customer']['Id']

		loggedin_headers['GO-SessionId'] = str(sessionId)
		loggedin_headers['GO-Token'] = str(goToken)
		loggedin_headers['GO-CustomerId'] = str(GOcustomerId)






def CATEGORIES():
	addDir('Filmek, sorozatok keresése ...','search','',4,'')

	req = urllib2.Request('https://huapi.hbogo.eu/v5/Groups/json/HUN/COMP', None, loggedin_headers)
	opener = urllib2.build_opener()
	f = opener.open(req)
	jsonrsp = json.loads(f.read())

	try:
		if jsonrsp['ErrorMessage']:
			xbmcgui.Dialog().ok('Hiba', jsonrsp['ErrorMessage'])
	except:
		pass
	
	for cat in range(0, len(jsonrsp['Items'])):
		addDir(jsonrsp['Items'][cat]['Name'].encode('utf-8', 'ignore'),jsonrsp['Items'][cat]['ObjectUrl'].replace('/0/{sort}/{pageIndex}/{pageSize}/0/0','/0/0/1/1024/0/0'),'',1,md+'DefaultFolder.png')





def LIST(url):
	req = urllib2.Request(url, None, loggedin_headers)
	opener = urllib2.build_opener()
	f = opener.open(req)
	jsonrsp = json.loads(f.read())

	try:
		if jsonrsp['ErrorMessage']:
			xbmcgui.Dialog().ok('Hiba', jsonrsp['ErrorMessage'])
	except:
		pass
	# If there is a subcategory / genres
	if len(jsonrsp['Container']) > 1:
		for Container in range(0, len(jsonrsp['Container'])):
			addDir(jsonrsp['Container'][Container]['Name'].encode('utf-8', 'ignore'),jsonrsp['Container'][Container]['ObjectUrl'],'',1,md+'DefaultFolder.png')
	else:
		for titles in range(0, len(jsonrsp['Container'][0]['Contents']['Items'])):
			if jsonrsp['Container'][0]['Contents']['Items'][titles]['ContentType'] == 1: #1=MOVIE/EXTRAS, 2=SERIES(serial), 3=SERIES(episode)
				#Ако е филм    # addLink(ou,plot,ar,imdb,bu,cast,director,writer,duration,genre,name,on,py,mode)
				plot = jsonrsp['Container'][0]['Contents']['Items'][titles]['Abstract'].encode('utf-8', 'ignore')
				if jsonrsp['Container'][0]['Contents']['Items'][titles]['AvailabilityTo'] is not None:
					plot = plot + ' Филма е достъпен за гледане до: ' + jsonrsp['Container'][0]['Contents']['Items'][titles]['AvailabilityTo'].encode('utf-8', 'ignore')
				addLink(jsonrsp['Container'][0]['Contents']['Items'][titles]['ObjectUrl'],plot,jsonrsp['Container'][0]['Contents']['Items'][titles]['AgeRating'],jsonrsp['Container'][0]['Contents']['Items'][titles]['ImdbRate'],jsonrsp['Container'][0]['Contents']['Items'][titles]['BackgroundUrl'],[jsonrsp['Container'][0]['Contents']['Items'][titles]['Cast'].split(', ')][0],jsonrsp['Container'][0]['Contents']['Items'][titles]['Director'],jsonrsp['Container'][0]['Contents']['Items'][titles]['Writer'],jsonrsp['Container'][0]['Contents']['Items'][titles]['Duration'],jsonrsp['Container'][0]['Contents']['Items'][titles]['Genre'],jsonrsp['Container'][0]['Contents']['Items'][titles]['Name'].encode('utf-8', 'ignore'),jsonrsp['Container'][0]['Contents']['Items'][titles]['OriginalName'],jsonrsp['Container'][0]['Contents']['Items'][titles]['ProductionYear'],5)
				#xbmc.log("GO: FILMI: DUMP: " + jsonrsp['Container'][0]['Contents']['Items'][titles]['ObjectUrl'], xbmc.LOGNOTICE)
				
			elif jsonrsp['Container'][0]['Contents']['Items'][titles]['ContentType'] == 3:
				#Ако е епизод на сериал    # addLink(ou,plot,ar,imdb,bu,cast,director,writer,duration,genre,name,on,py,mode)
				plot = jsonrsp['Container'][0]['Contents']['Items'][titles]['Abstract'].encode('utf-8', 'ignore')
				if jsonrsp['Container'][0]['Contents']['Items'][titles]['AvailabilityTo'] is not None:
					plot = plot + ' Епизода е достъпен за гледане до: ' + jsonrsp['Container'][0]['Contents']['Items'][titles]['AvailabilityTo'].encode('utf-8', 'ignore')
				addLink(jsonrsp['Container'][0]['Contents']['Items'][titles]['ObjectUrl'],plot,jsonrsp['Container'][0]['Contents']['Items'][titles]['AgeRating'],jsonrsp['Container'][0]['Contents']['Items'][titles]['ImdbRate'],jsonrsp['Container'][0]['Contents']['Items'][titles]['BackgroundUrl'],[jsonrsp['Container'][0]['Contents']['Items'][titles]['Cast'].split(', ')][0],jsonrsp['Container'][0]['Contents']['Items'][titles]['Director'],jsonrsp['Container'][0]['Contents']['Items'][titles]['Writer'],jsonrsp['Container'][0]['Contents']['Items'][titles]['Duration'],jsonrsp['Container'][0]['Contents']['Items'][titles]['Genre'],jsonrsp['Container'][0]['Contents']['Items'][titles]['SeriesName'].encode('utf-8', 'ignore')+' СЕЗОН '+str(jsonrsp['Container'][0]['Contents']['Items'][titles]['SeasonIndex'])+' ЕПИЗОД '+str(jsonrsp['Container'][0]['Contents']['Items'][titles]['Index']),jsonrsp['Container'][0]['Contents']['Items'][titles]['OriginalName'],jsonrsp['Container'][0]['Contents']['Items'][titles]['ProductionYear'],5)
			else:
				#Ако е сериал
				addDir(jsonrsp['Container'][0]['Contents']['Items'][titles]['Name'].encode('utf-8', 'ignore'),jsonrsp['Container'][0]['Contents']['Items'][titles]['ObjectUrl'],jsonrsp['Container'][0]['Contents']['Items'][titles]['Abstract'].encode('utf-8', 'ignore'),2,jsonrsp['Container'][0]['Contents']['Items'][titles]['BackgroundUrl'])



def SEASON(url):
	req = urllib2.Request(url, None, loggedin_headers)
	opener = urllib2.build_opener()
	f = opener.open(req)
	jsonrsp = json.loads(f.read())

	try:
		if jsonrsp['ErrorMessage']:
			xbmcgui.Dialog().ok('Hiba', jsonrsp['ErrorMessage'])
	except:
		pass
	for season in range(0, len(jsonrsp['Parent']['ChildContents']['Items'])):
		addDir(jsonrsp['Parent']['ChildContents']['Items'][season]['Name'].encode('utf-8', 'ignore'),jsonrsp['Parent']['ChildContents']['Items'][season]['ObjectUrl'],jsonrsp['Parent']['ChildContents']['Items'][season]['Abstract'].encode('utf-8', 'ignore'),3,jsonrsp['Parent']['ChildContents']['Items'][season]['BackgroundUrl'])




def EPISODE(url):
	req = urllib2.Request(url, None, loggedin_headers)
	opener = urllib2.build_opener()
	f = opener.open(req)
	jsonrsp = json.loads(f.read())

	try:
		if jsonrsp['ErrorMessage']:
			xbmcgui.Dialog().ok('Hiba', jsonrsp['ErrorMessage'])
	except:
		pass

	for episode in range(0, len(jsonrsp['ChildContents']['Items'])):
		# addLink(ou,plot,ar,imdb,bu,cast,director,writer,duration,genre,name,on,py,mode)
		plot = jsonrsp['ChildContents']['Items'][episode]['Abstract'].encode('utf-8', 'ignore')
		if jsonrsp['ChildContents']['Items'][episode]['AvailabilityTo'] is not None:
			plot = plot + ' Епизода е достъпен за гледане до: ' + jsonrsp['ChildContents']['Items'][episode]['AvailabilityTo'].encode('utf-8', 'ignore')
		addLink(jsonrsp['ChildContents']['Items'][episode]['ObjectUrl'],plot,jsonrsp['ChildContents']['Items'][episode]['AgeRating'],jsonrsp['ChildContents']['Items'][episode]['ImdbRate'],jsonrsp['ChildContents']['Items'][episode]['BackgroundUrl'],[jsonrsp['ChildContents']['Items'][episode]['Cast'].split(', ')][0],jsonrsp['ChildContents']['Items'][episode]['Director'],jsonrsp['ChildContents']['Items'][episode]['Writer'],jsonrsp['ChildContents']['Items'][episode]['Duration'],jsonrsp['ChildContents']['Items'][episode]['Genre'],jsonrsp['ChildContents']['Items'][episode]['SeriesName'].encode('utf-8', 'ignore')+' СЕЗОН '+str(jsonrsp['ChildContents']['Items'][episode]['SeasonIndex'])+' '+jsonrsp['ChildContents']['Items'][episode]['Name'].encode('utf-8', 'ignore'),jsonrsp['ChildContents']['Items'][episode]['OriginalName'],jsonrsp['ChildContents']['Items'][episode]['ProductionYear'],5)


def PLAY(url):
	global goToken
	global individualization
	global customerId
	global GOcustomerId
	global sessionId
	global loggedin_headers


	if sessionId == '00000000-0000-0000-0000-000000000000':
		LOGIN()
	
	if se=='true':
		try:
			#print 'CID '+cid
			#http://huapi.hbogo.eu/player50.svc/Content/json/HUN/COMP/
			#http://huapi.hbogo.eu/player50.svc/Content/json/HUN/APPLE/
			#http://huapi.hbogo.eu/player50.svc/Content/json/HUN/SONY/
			req = urllib2.Request('http://huapi.hbogo.eu/v5/Content/json/HUN/MOBI/'+cid, None, loggedin_headers)
			req.add_header('User-Agent', MUA)
			opener = urllib2.build_opener()
			f = opener.open(req)
			jsonrsps = json.loads(f.read())
			#print jsonrsps
			
			try:
				if jsonrsps['Subtitles'][0]['Code']==Code:
					slink = jsonrsps['Subtitles'][0]['Url']
				elif jsonrsps['Subtitles'][1]['Code']==Code:
					slink = jsonrsps['Subtitles'][1]['Url']
				req = urllib2.Request(slink, None, loggedin_headers)
				response = urllib2.urlopen(req)
				data=response.read()
				response.close()
					
				subs = re.compile('<p[^>]+begin="([^"]+)\D(\d+)"[^>]+end="([^"]+)\D(\d+)"[^>]*>([\w\W]+?)</p>').findall(data)
				row = 0
				buffer = ''
				for sub in subs:
					row = row + 1
					buffer += str(row) +'\n'
					buffer += "%s,%03d" % (sub[0], int(sub[1])) + ' --> ' + "%s,%03d" % (sub[2], int(sub[3])) + '\n'
					buffer += urllib.unquote_plus(sub[4]).replace('<br/>','\n').replace('<br />','\n').replace("\r\n", "").replace("&lt;", "<").replace("&gt;", ">").replace("\n    ","").strip()
					buffer += '\n\n'
					sub = 'true'
					with open(srtsubs_path, "w") as subfile:
						subfile.write(buffer)

				if sub != 'true':
					raise Exception()
					
			except:
				sub = 'false'
		except:
			sub = 'false'
	
	

	purchase_payload = '<Purchase xmlns="go:v5:interop"><AllowHighResolution>true</AllowHighResolution><ContentId>'+cid+'</ContentId><CustomerId>'+GOcustomerId+'</CustomerId><Individualization>'+individualization+'</Individualization><OperatorId>'+op_id+'</OperatorId><ClientInfo></ClientInfo><IsFree>false</IsFree><UseInteractivity>false</UseInteractivity></Purchase>'

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
		'Host': 'huapi.hbogo.eu',
		'Referer': 'https://hbogo.hu/',
		'Origin': 'https://www.hbogo.hu',
		'User-Agent': UA
		}

	req = urllib2.Request('https://huapi.hbogo.eu/v5/Purchase/Json/HUN/COMP', purchase_payload, purchase_headers)
	opener = urllib2.build_opener()
	f = opener.open(req)
	jsonrspp = json.loads(f.read())
	print jsonrspp

	try:
		if jsonrspp['ErrorMessage']:
			xbmcgui.Dialog().ok('Hiba', jsonrspp['ErrorMessage'])
	except:
		pass

	MediaUrl = jsonrspp['Purchase']['MediaUrl'] + "/Manifest"
	PlayerSessionId = jsonrspp['Purchase']['PlayerSessionId']
	x_dt_auth_token = jsonrspp['Purchase']['AuthToken']
	dt_custom_data = base64.b64encode("{\"userId\":\"" + GOcustomerId + "\",\"sessionId\":\"" + PlayerSessionId + "\",\"merchant\":\"hboeurope\"}")


	li = xbmcgui.ListItem(iconImage=thumbnail, thumbnailImage=thumbnail, path=MediaUrl)
	if (se=='true' and sub=='true'): 
		li.setSubtitles([srtsubs_path])
	license_server = 'https://lic.drmtoday.com/license-proxy-widevine/cenc/'
	license_headers = 'dt-custom-data=' + dt_custom_data + '&x-dt-auth-token=' + x_dt_auth_token + '&Origin=https://www.hbogo.hu&Content-Type='
	license_key = license_server + '|' + license_headers + '|R{SSM}|JBlicense'

	li.setProperty('inputstreamaddon', 'inputstream.adaptive')
	li.setProperty('inputstream.adaptive.manifest_type', 'ism')
	li.setProperty('inputstream.adaptive.license_type', 'com.widevine.alpha')
	li.setProperty('inputstream.adaptive.license_data', 'ZmtqM2xqYVNkZmFsa3Izag==')
	li.setProperty('inputstream.adaptive.license_key', license_key)
	
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, li)

	#Задаване на външни субтитри, ако е избран този режим
	#if (se=='true' and sub=='true'):
	#	while not xbmc.Player().isPlaying():
	#		xbmc.sleep(42)
	#		xbmc.Player().setSubtitles(srtsubs_path)



def SEARCH():
	keyb = xbmc.Keyboard(search_string, 'Filmek, sorozatok keresése ...')
	keyb.doModal()
	searchText = ''
	if (keyb.isConfirmed()):
		searchText = urllib.quote_plus(keyb.getText())
		if searchText == "":
			addDir('Nincs találat','','','',md+'DefaultFolderBack.png')
		else:
			__settings__.setSetting('lastsearch', searchText)

			req = urllib2.Request('https://huapi.hbogo.eu/v5/Search/Json/HUN/COMP/'+searchText.decode('utf-8', 'ignore').encode('utf-8', 'ignore')+'/0', None, loggedin_headers)
			opener = urllib2.build_opener()
			f = opener.open(req)
			jsonrsp = json.loads(f.read())        
			#print jsonrsp

			try:
				if jsonrsp['ErrorMessage']:
					xbmcgui.Dialog().ok('Hiba', jsonrsp['ErrorMessage'])
			except:
				pass

			br=0
			for index in range(0, len(jsonrsp['Container'][0]['Contents']['Items'])):
				if (jsonrsp['Container'][0]['Contents']['Items'][index]['ContentType'] == 1 or jsonrsp['Container'][0]['Contents']['Items'][index]['ContentType'] == 7): #1,7=MOVIE/EXTRAS, 2=SERIES(serial), 3=SERIES(episode)
					#Ако е филм    # addLink(ou,plot,ar,imdb,bu,cast,director,writer,duration,genre,name,on,py,mode)
					addLink(jsonrsp['Container'][0]['Contents']['Items'][index]['ObjectUrl'],jsonrsp['Container'][0]['Contents']['Items'][index]['Abstract'].encode('utf-8', 'ignore'),jsonrsp['Container'][0]['Contents']['Items'][index]['AgeRating'],jsonrsp['Container'][0]['Contents']['Items'][index]['ImdbRate'],jsonrsp['Container'][0]['Contents']['Items'][index]['BackgroundUrl'],[jsonrsp['Container'][0]['Contents']['Items'][index]['Cast'].split(', ')][0],jsonrsp['Container'][0]['Contents']['Items'][index]['Director'],jsonrsp['Container'][0]['Contents']['Items'][index]['Writer'],jsonrsp['Container'][0]['Contents']['Items'][index]['Duration'],jsonrsp['Container'][0]['Contents']['Items'][index]['Genre'],jsonrsp['Container'][0]['Contents']['Items'][index]['Name'].encode('utf-8', 'ignore'),jsonrsp['Container'][0]['Contents']['Items'][index]['OriginalName'],jsonrsp['Container'][0]['Contents']['Items'][index]['ProductionYear'],5)
				elif jsonrsp['Container'][0]['Contents']['Items'][index]['ContentType'] == 3:
					#Ако е епизод на сериал    # addLink(ou,plot,ar,imdb,bu,cast,director,writer,duration,genre,name,on,py,mode)
					addLink(jsonrsp['Container'][0]['Contents']['Items'][index]['ObjectUrl'],jsonrsp['Container'][0]['Contents']['Items'][index]['Abstract'].encode('utf-8', 'ignore'),jsonrsp['Container'][0]['Contents']['Items'][index]['AgeRating'],jsonrsp['Container'][0]['Contents']['Items'][index]['ImdbRate'],jsonrsp['Container'][0]['Contents']['Items'][index]['BackgroundUrl'],[jsonrsp['Container'][0]['Contents']['Items'][index]['Cast'].split(', ')][0],jsonrsp['Container'][0]['Contents']['Items'][index]['Director'],jsonrsp['Container'][0]['Contents']['Items'][index]['Writer'],jsonrsp['Container'][0]['Contents']['Items'][index]['Duration'],jsonrsp['Container'][0]['Contents']['Items'][index]['Genre'],jsonrsp['Container'][0]['Contents']['Items'][index]['SeriesName'].encode('utf-8', 'ignore')+' '+jsonrsp['Container'][0]['Contents']['Items'][index]['Name'].encode('utf-8', 'ignore'),jsonrsp['Container'][0]['Contents']['Items'][index]['OriginalName'],jsonrsp['Container'][0]['Contents']['Items'][index]['ProductionYear'],5)
				else:
					#Ако е сериал
					addDir(jsonrsp['Container'][0]['Contents']['Items'][index]['Name'].encode('utf-8', 'ignore'),jsonrsp['Container'][0]['Contents']['Items'][index]['ObjectUrl'],jsonrsp['Container'][0]['Contents']['Items'][index]['Abstract'].encode('utf-8', 'ignore'),2,jsonrsp['Container'][0]['Contents']['Items'][index]['BackgroundUrl'])
				br=br+1
			if br==0:
				addDir('Nincs találat','','','',md+'DefaultFolderBack.png')

		





def addLink(ou,plot,ar,imdb,bu,cast,director,writer,duration,genre,name,on,py,mode):
	cid = ou.rsplit('/',2)[1]
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)+"&cid="+cid+"&thumbnail="+bu
	ok=True
	liz=xbmcgui.ListItem(name, iconImage=bu, thumbnailImage=bu)
	liz.setArt({ 'thumb': bu,'poster': bu, 'banner' : bu, 'fanart': bu })
	liz.setInfo( type="Video", infoLabels={ "plot": plot, "mpaa": str(ar)+'+', "rating": imdb, "cast": cast, "director": director, "writer": writer, "duration": duration, "genre": genre, "title": name, "originaltitle": on, "year": py } )
	liz.addStreamInfo('video', { 'width': 1280, 'height': 720 })
	liz.addStreamInfo('video', { 'aspect': 1.78, 'codec': 'h264' })
	liz.addStreamInfo('audio', { 'codec': 'aac', 'channels': 2 })
	liz.setProperty("IsPlayable" , "true")
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=False)
	return ok


def addDir(name,url,plot,mode,iconimage):
	u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
	ok=True
	liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
	liz.setInfo( type="Video", infoLabels={ "Title": name, "Plot": plot } )
	ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
	return ok



def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param



params=get_params()
url=None
name=None
iconimage=None
mode=None

try:
		url=urllib.unquote_plus(params["url"])
except:
		pass
try:
		name=urllib.unquote_plus(params["name"])
except:
		pass
try:
		thumbnail=str(params["thumbnail"])
except:
		pass
try:
		mode=int(params["mode"])
except:
		pass
try:
		cid=str(params["cid"])
except:
		pass



if mode==None or url==None or len(url)<1:
		CATEGORIES()

elif mode==1:
		LIST(url)

elif mode==2:
		SEASON(url)

elif mode==3:
		EPISODE(url)

elif mode==4:
		SEARCH()

elif mode==5:
		PLAY(url)

elif mode==6:
		SILENTREGISTER()

elif mode==7:
		LOGIN()


xbmcplugin.endOfDirectory(int(sys.argv[1]))
