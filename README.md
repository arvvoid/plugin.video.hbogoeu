# Disclaimer

This add-on is not officially commissioned/supported by HBO®. The trademark HBO® Go is registered by Home Box Office, Inc.
For more information on HBO® Go Europe visit the official website: http://hbogo.eu

This is also not an "official Add-on" by the Kodi team. I have no affiliation with the Kodi team.

THERE IS NO WARRANTY FOR THE ADD-ON, IT CAN BREAK AND STOP WORKING AT ANY TIME.

If an official app is available for your platform, use it instead of this.

# HBO GO Europe for Kodi 18 (plugin.video.hbogoeu)

Simple, great Kodi add-on to access HBO® Go Europe content (http://hbogo.eu) from Kodi Media Center (http://kodi.tv).

Important, HBO® Go must be paid for!!! You need a valid HBO® Go account for the add-on to work!
Register on the official HBO® Go website http://hbogo.eu

This add-on covers all listend on http://hbogo.eu or sharing the same api atm 13 countries: 
* Bosnia and Herzegovina
* Bulgaria
* Croatia
* Czech Republic 
* Hungary
* Macedonia 
* Montenegro
* Polonia
* Portugal
* Romania
* Serbia
* Slovakia
* Slovenija

Other Hbo Go versions/regions that use diferent APIs, are currently not covered by this add-on, but there is hope for future support and transforming this in a general hbogo add-on, but that will take time and collaboration with local developers using and having access to those services:

* HBO España (https://en.hboespana.com/) [NOT SUPPORTED BY THIS ADD-ON] [#6](https://github.com/arvvoid/plugin.video.hbogoeu/issues/6)
* HBO Nordic (https://www.hbonordic.com/)  [NOT SUPPORTED BY THIS ADD-ON] [#7](https://github.com/arvvoid/plugin.video.hbogoeu/issues/7)
* HBO Go US (http://hbogo.com)  [NOT SUPPORTED BY THIS ADD-ON] [#8](https://github.com/arvvoid/plugin.video.hbogoeu/issues/8)
* HBO Go Asia (https://www.hbogoasia.com/)  [NOT SUPPORTED BY THIS ADD-ON] [#8](https://github.com/arvvoid/plugin.video.hbogoeu/issues/8)
* HBO Go Latin America (https://www.hbogo.com.br/)  [NOT SUPPORTED BY THIS ADD-ON] [#8](https://github.com/arvvoid/plugin.video.hbogoeu/issues/8)

PLEASE IF YOU ARE REPORTING AN ISSUE PROVIDE Kodi Debug Logs: https://kodi.wiki/view/Log_file/Easy . Without a full log is difficult or impossible to guess what's going on.

REQUIRMENTS:
* Kodi 18+
* script.module.requests 2.12.4+ (should get installed automatically in Kodi 18)
* script.module.pycryptodome 3.4.3+ (should get installed automatically in Kodi 18)
* inputstream.adaptive 2.3.15+ (should get installed automatically in Kodi 18)
* script.module.inputstreamhelper 0.3.3+ (should get installed automatically in Kodi 18)
* Libwidevine (Your device might include it already or might not, not all devices have the same widevine certification level, witch can impact playback ability and max quality of DRM content, please make sure to read the licence agreement that comes with it, so you know what you´re getting yourself into.) 
* playback quality (resolution) of DRM content in Kodi, and if the playback will work at all, depends on Inputstream Adaptive and Libwidevine and widevine certification level on your device, and the service provider requirments and restrictions for the specific content. HDCP support can play a role as well.

Initial version was derived from https://github.com/billsuxx/plugin.video.hbogohu witch is derived from https://kodibg.org/forum/thread-504.html, this now is a complete rewrite and restructure of the add-on.

## Download

Download [repository.arvvoid-1.0.0.zip](https://raw.github.com/arvvoid/repository.arvvoid/master/repository.arvvoid/repository.arvvoid-1.0.0.zip) and use the install add-on from zip function in Kodi
 then follow the install instructions

## Install instructions

* Enable Input Stream Add-on in Kodi v18+: Add-ons >> Package icon >> My Add-ons >> Video Player Inputstream >> Inputstream Adaptive >> menu >> enable
* Install the add-on from repository "Kodi ArvVoid Repository"
* Configure the Add-on: select the correct operator and enter your hbogo username and password 
(first check if you can login in your local hbo go website without problems)
* The Add-on should download the inputstreamhelper Add-on which will handle all the DRM install for you if needed

## Latest relese

[plugin.video.hbogoeu-2.0.7~beta19.zip](https://github.com/arvvoid/repository.arvvoid/raw/master/plugin.video.hbogoeu/plugin.video.hbogoeu-2.0.7~beta19.zip)

[CHANGE LOG](https://github.com/arvvoid/plugin.video.hbogoeu/blob/master/changelog.md)

## Help

Join the discusion on the [Kodi Forum](https://forum.kodi.tv/showthread.php?tid=339798), if you have a bug or issue to report open a new [ISSUE](https://github.com/arvvoid/plugin.video.hbogoeu/issues)

## Video Demo and Install instructions

[![Watch the video](https://img.youtube.com/vi/m326rV0vH8Q/hqdefault.jpg)](https://youtu.be/m326rV0vH8Q)
