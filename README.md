# Disclaimer

This add-on is not officially commissioned/supported by HBO®. The trademark HBO® Go is registered by Home Box Office, Inc.
For more information visit the official HBO® Go website for your region.

This is also not an "official Add-on" by the Kodi team. I have no affiliation with the Kodi team.

THERE IS NO WARRANTY FOR THE ADD-ON, IT CAN BREAK AND STOP WORKING AT ANY TIME.

If an official app is available for your platform, use it instead of this.

Important: HBO® Go must be paid for!!! You need a valid HBO® Go account for the add-on to work!
Register on the official HBO® Go website for your region

# HBO GO Europe for Kodi 18 (plugin.video.hbogoeu)

Simple, great Kodi add-on to access HBO® Go content from Kodi Media Center (http://kodi.tv).

| REGION / Feature           | HBO GO EU | HBO Spain + Nordic | HBO USA | HBO Latin America | HBO Asia |
|----------------------------|-----------|--------------------|---------|-------------------|----------|
| Listing Content            | STABLE    | STABLE             | N/A     | N/A               | N/A      |
| Content Info               | STABLE    | STABLE             | N/A     | N/A               | N/A      |
| Search                     | STABLE    | N/A                | N/A     | N/A               | N/A      |
| Login                      | STABLE    | STABLE             | N/A     | N/A               | N/A      |
| Playback                   | STABLE    | STABLE             | N/A     | N/A               | N/A      |
| Subtitles                  | STABLE    | STABLE             | N/A     | N/A               | N/A      |
| My List                    | STABLE    | N/A                | N/A     | N/A               | N/A      |
| Add/Remove from My List    | STABLE    | N/A                | N/A     | N/A               | N/A      |
| Voting                     | STABLE    | N/A                | N/A     | N/A               | N/A      |
| Report play  status to HBO | N/A       | N/A                | N/A     | N/A               | N/A      |


This add-on support 18 countries atm: 
* __Bosnia and Herzegovina__ *[HBO Go EU]* 
* __Bulgaria__ *[HBO Go EU]* 
* __Croatia__ *[HBO Go EU]* 
* __Czech Republic__ *[HBO Go EU]*  (Skylink, UPC CZ are currently not working with the add-on [#5](https://github.com/arvvoid/plugin.video.hbogoeu/issues/5))
* __Hungary__ *[HBO Go EU]* 
* __Macedonia__ *[HBO Go EU]* 
* __Montenegro__ *[HBO Go EU]* 
* __Polonia__ *[HBO Go EU]* 
* __Portugal__ *[HBO Go EU]* 
* __Romania__ *[HBO Go EU]*  (Telekom Romania, UPC Romania, Vodafone Romania 4GTV+ are currently not working with the add-on [#5](https://github.com/arvvoid/plugin.video.hbogoeu/issues/5))
* __Serbia__ *[HBO Go EU]* 
* __Slovakia__ *[HBO Go EU]*  (Skylink, UPC CZ are currently not working with the add-on [#5](https://github.com/arvvoid/plugin.video.hbogoeu/issues/5))
* __Slovenija__ *[HBO Go EU]* 
* __Spain__ *[HBO Spain]* 
* __Norway__ *[HBO Nordic]* 
* __Denmark__ *[HBO Nordic]* 
* __Sweden__ *[HBO Nordic]* 
* __Finland__ *[HBO Nordic]*

PLEASE IF YOU ARE REPORTING AN ISSUE PROVIDE Kodi Debug Logs: https://kodi.wiki/view/Log_file/Easy . Without a full log is difficult or impossible to guess what's going on.

REQUIRMENTS:
* Kodi 18+
* script.module.requests 2.12.4+ (should get installed automatically in Kodi 18)
* script.module.pycryptodome 3.4.3+ (should get installed automatically in Kodi 18)
* inputstream.adaptive 2.3.19+ (should get installed automatically in Kodi 18)
* script.module.inputstreamhelper 0.3.5+ (should get installed automatically in Kodi 18)
* Libwidevine 4.10.1440+

Initial version was derived from https://github.com/billsuxx/plugin.video.hbogohu witch is derived from https://kodibg.org/forum/thread-504.html, this now is a complete rewrite and restructure of the add-on.

## Download

Download [repository.arvvoid-1.0.0.zip](https://raw.github.com/arvvoid/repository.arvvoid/master/repository.arvvoid/repository.arvvoid-1.0.0.zip) and use the install add-on from zip function in Kodi
 then follow the install instructions

## Install instructions

* *OPTIONAL: On OSMC/Raspbian you might have to install some dependency manualy from shell:*
```
sudo apt update
sudo apt install python-pip
sudo apt install python-setuptools
sudo apt install build-essential
sudo pip install wheel
sudo pip install pycryptodomex
sudo apt install libnss3 libnspr4
sudo reboot
```
* Install the add-on from repository "Kodi ArvVoid Repository"
* Follow the setup wizard at first add-on run
* *OPTIONAL: Configure additional preferences in the add-on config*
* The Add-on should download the inputstreamhelper Add-on which will handle all the DRM install for you if needed

## Latest relese

[plugin.video.hbogoeu-2.0.12~beta28.zip](https://github.com/arvvoid/repository.arvvoid/raw/master/plugin.video.hbogoeu/plugin.video.hbogoeu-2.0.12~beta28.zip)

[CHANGE LOG](https://github.com/arvvoid/plugin.video.hbogoeu/blob/master/changelog.md)

## Help

Join the discusion on the [Kodi Forum](https://forum.kodi.tv/showthread.php?tid=339798), if you have a bug or issue to report open a new [ISSUE](https://github.com/arvvoid/plugin.video.hbogoeu/issues)

## Video Demo and Install instructions

[![Watch the video](https://img.youtube.com/vi/m326rV0vH8Q/hqdefault.jpg)](https://youtu.be/m326rV0vH8Q)
