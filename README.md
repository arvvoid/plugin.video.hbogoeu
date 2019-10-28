[![GitHub issues](https://img.shields.io/github/issues/arvvoid/plugin.video.hbogoeu?style=flat)](https://github.com/arvvoid/plugin.video.hbogoeu/issues) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/9168cc04d56d480ea3987db569d89f44)](https://www.codacy.com/manual/arvvoid/plugin.video.hbogoeu?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=arvvoid/plugin.video.hbogoeu&amp;utm_campaign=Badge_Grade) [![GitHub last commit](https://img.shields.io/github/last-commit/arvvoid/plugin.video.hbogoeu?style=flat)](https://github.com/arvvoid/plugin.video.hbogoeu/commits/master) [![GitHub (Pre-)Release Date](https://img.shields.io/github/release-date-pre/arvvoid/plugin.video.hbogoeu?label=last%20pre-release&style=flat)](#pre-rel) [![GitHub Release Date](https://img.shields.io/github/release-date/arvvoid/plugin.video.hbogoeu?style=flat)](#release) [![GitHub](https://img.shields.io/github/license/arvvoid/plugin.video.hbogoeu?style=flat)](https://opensource.org/licenses/gpl-2.0.php) [![Contributors](https://img.shields.io/github/contributors/arvvoid/plugin.video.hbogoeu.svg)](https://github.com/arvvoid/plugin.video.hbogoeu/graphs/contributors) [![All Contributors](https://img.shields.io/badge/all_contributors-9-orange.svg?style=flat-square)](#contributors) [![HitCount](http://hits.dwyl.io/arvvoid/pluginvideohbogoeu.svg)](http://hits.dwyl.io/arvvoid/pluginvideohbogoeu)


# Disclaimer

This add-on is not officially commissioned/supported by HBO®. The trademark HBO® Go is registered by Home Box Office, Inc.
For more information visit the official HBO® Go website for your region.

This is also not an "official Add-on" by the Kodi team. I have no affiliation with the Kodi team.

THERE IS NO WARRANTY FOR THE ADD-ON, IT CAN BREAK AND STOP WORKING AT ANY TIME.

If an official app is available for your platform, use it instead of this.

Important: HBO® Go must be paid for!!! You need a valid HBO® Go account for the add-on to work!
Register on the official HBO® Go website for your region

# HBO GO Europe for Kodi (plugin.video.hbogoeu)

Simple, Kodi add-on to access HBO® Go content from Kodi Media Center (http://kodi.tv).

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
*  __Bosnia and Herzegovina__ *[HBO Go EU]* 
*  __Bulgaria__ *[HBO Go EU]* 
*  __Croatia__ *[HBO Go EU]* 
*  __Czech Republic__ *[HBO Go EU]*  (Skylink, UPC CZ are currently not working with the add-on [#5](https://github.com/arvvoid/plugin.video.hbogoeu/issues/5))
*  __Hungary__ *[HBO Go EU]* 
*  __Macedonia__ *[HBO Go EU]* 
*  __Montenegro__ *[HBO Go EU]* 
*  __Polonia__ *[HBO Go EU]* 
*  __Portugal__ *[HBO Go EU]* 
*  __Romania__ *[HBO Go EU]*  (Telekom Romania, UPC Romania, Vodafone Romania 4GTV+ are currently not working with the add-on [#5](https://github.com/arvvoid/plugin.video.hbogoeu/issues/5))
*  __Serbia__ *[HBO Go EU]* 
*  __Slovakia__ *[HBO Go EU]*  (Skylink, UPC CZ are currently not working with the add-on [#5](https://github.com/arvvoid/plugin.video.hbogoeu/issues/5))
*  __Slovenija__ *[HBO Go EU]* 
*  __Spain__ *[HBO Spain]* 
*  __Norway__ *[HBO Nordic]* 
*  __Denmark__ *[HBO Nordic]* 
*  __Sweden__ *[HBO Nordic]* 
*  __Finland__ *[HBO Nordic]*

PLEASE IF YOU ARE REPORTING AN ISSUE PROVIDE Kodi Debug Logs: https://kodi.wiki/view/Log_file/Easy . Without a full log is difficult or impossible to guess what's going on.

REQUIRMENTS:
*  Kodi 18+
*  script.module.kodi-six (should get installed automatically in Kodi 18)
*  script.module.requests 2.12.4+ (should get installed automatically in Kodi 18)
*  script.module.pycryptodome 3.4.3+ (should get installed automatically in Kodi 18)
*  script.module.defusedxml 0.6.0+ (should get installed automatically in Kodi 18)
*  inputstream.adaptive 2.3.18+ (recommended most recent version, should get installed automatically in Kodi 18)
*  script.module.inputstreamhelper 0.4.2+ (should get installed automatically in Kodi 18)
*  Libwidevine 4.10.1440+

## Download/Install instructions

* Download [repository.arvvoid-1.0.0.zip](https://raw.github.com/arvvoid/repository.arvvoid/master/repository.arvvoid/repository.arvvoid-1.0.0.zip) and use the install add-on from zip function in Kodi
* Install the add-on from repository "Kodi ArvVoid Repository"
* Follow the setup wizard at first add-on run
* *OPTIONAL: Configure additional preferences in the add-on config*
* The Add-on should download the inputstreamhelper Add-on which will handle all the DRM install for you if needed
* *OPTIONAL: On OSMC/Raspbian/Debian/Ubuntu/other Debian derivates you might have to install some dependency manually from shell, but first try to run the add-on, if you get a message informing you that pycryptodomex is missing perform this steps (or consult specific pycryptodomex install instructions for your distribution/platform):*
```
sudo apt update
sudo apt install build-essential python-setuptools python-pip libnss3 libnspr4
sudo pip install wheel pycryptodomex
```

## Latest relese

[plugin.video.hbogoeu-2.0.19~beta38.zip](https://github.com/arvvoid/repository.arvvoid/raw/master/plugin.video.hbogoeu/plugin.video.hbogoeu-2.0.19~beta38.zip)

[CHANGE LOG](https://github.com/arvvoid/plugin.video.hbogoeu/blob/master/changelog.md)

## Help

Join the discusion on the [Kodi Forum](https://forum.kodi.tv/showthread.php?tid=339798), if you have a bug or issue to report open a new [ISSUE](https://github.com/arvvoid/plugin.video.hbogoeu/issues)

## Video Demo and Install instructions

[![Watch the video](https://img.youtube.com/vi/m326rV0vH8Q/hqdefault.jpg)](https://youtu.be/m326rV0vH8Q)

## History

Initial version was derived from https://github.com/billsuxx/plugin.video.hbogohu witch is derived from https://kodibg.org/forum/thread-504.html, this now is a complete rewrite and restructure of the add-on.

## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):

<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/arvvoid"><img src="https://avatars2.githubusercontent.com/u/46710439?v=4" width="100px;" alt="Arv.Void"/><br /><sub><b>Arv.Void</b></sub></a><br /><a href="https://github.com/arvvoid/plugin.video.hbogoeu/commits?author=arvvoid" title="Code">💻</a> <a href="https://github.com/arvvoid/plugin.video.hbogoeu/commits?author=arvvoid" title="Documentation">📖</a> <a href="#ideas-arvvoid" title="Ideas, Planning, & Feedback">🤔</a> <a href="#maintenance-arvvoid" title="Maintenance">🚧</a> <a href="#translation-arvvoid" title="Translation">🌍</a></td>
    <td align="center"><a href="https://github.com/billsuxx"><img src="https://avatars3.githubusercontent.com/u/4318995?v=4" width="100px;" alt="David Fodor"/><br /><sub><b>David Fodor</b></sub></a><br /><a href="https://github.com/arvvoid/plugin.video.hbogoeu/commits?author=billsuxx" title="Code">💻</a></td>
    <td align="center"><a href="https://github.com/Sakerdot"><img src="https://avatars3.githubusercontent.com/u/9504138?v=4" width="100px;" alt="Adrian Samatan"/><br /><sub><b>Adrian Samatan</b></sub></a><br /><a href="https://github.com/arvvoid/plugin.video.hbogoeu/commits?author=Sakerdot" title="Code">💻</a> <a href="#ideas-Sakerdot" title="Ideas, Planning, & Feedback">🤔</a></td>
    <td align="center"><a href="https://github.com/PolliSoft"><img src="https://avatars0.githubusercontent.com/u/563252?v=4" width="100px;" alt="Olof Sandberg"/><br /><sub><b>Olof Sandberg</b></sub></a><br /><a href="https://github.com/arvvoid/plugin.video.hbogoeu/issues?q=author%3APolliSoft" title="Bug reports">🐛</a> <a href="https://github.com/arvvoid/plugin.video.hbogoeu/commits?author=PolliSoft" title="Tests">⚠️</a></td>
    <td align="center"><a href="https://github.com/macardi"><img src="https://avatars0.githubusercontent.com/u/71271?v=4" width="100px;" alt="macardi"/><br /><sub><b>macardi</b></sub></a><br /><a href="#translation-macardi" title="Translation">🌍</a> <a href="https://github.com/arvvoid/plugin.video.hbogoeu/commits?author=macardi" title="Tests">⚠️</a></td>
    <td align="center"><a href="https://github.com/jhdgghost"><img src="https://avatars2.githubusercontent.com/u/25726039?v=4" width="100px;" alt="jhdgghost"/><br /><sub><b>jhdgghost</b></sub></a><br /><a href="#translation-jhdgghost" title="Translation">🌍</a> <a href="https://github.com/arvvoid/plugin.video.hbogoeu/commits?author=jhdgghost" title="Tests">⚠️</a></td>
    <td align="center"><a href="https://github.com/jumakki"><img src="https://avatars3.githubusercontent.com/u/32912134?v=4" width="100px;" alt="jumakki"/><br /><sub><b>jumakki</b></sub></a><br /><a href="#translation-jumakki" title="Translation">🌍</a> <a href="https://github.com/arvvoid/plugin.video.hbogoeu/commits?author=jumakki" title="Tests">⚠️</a> <a href="https://github.com/arvvoid/plugin.video.hbogoeu/issues?q=author%3Ajumakki" title="Bug reports">🐛</a> <a href="#ideas-jumakki" title="Ideas, Planning, & Feedback">🤔</a></td>
  </tr>
  <tr>
    <td align="center"><a href="https://github.com/sanangel"><img src="https://avatars1.githubusercontent.com/u/20192587?v=4" width="100px;" alt="sanangel"/><br /><sub><b>sanangel</b></sub></a><br /><a href="https://github.com/arvvoid/plugin.video.hbogoeu/commits?author=sanangel" title="Tests">⚠️</a></td>
    <td align="center"><a href="http://www.el-magnifico.org"><img src="https://avatars0.githubusercontent.com/u/697599?v=4" width="100px;" alt="Alfonso E.M."/><br /><sub><b>Alfonso E.M.</b></sub></a><br /><a href="https://github.com/arvvoid/plugin.video.hbogoeu/commits?author=alfem" title="Tests">⚠️</a></td>
  </tr>
</table>

<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
