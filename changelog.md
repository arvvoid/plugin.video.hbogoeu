v.2.7.8
- Fixes "new version" errors on series/season listings

v.2.7.4
- Hot Fix: fix playback going throu TV Shows or Movies category [EU region]
- Remove obsolete non standard login redirect methods (no longer needed and abandoned by all operators) [EU region]
- Change fallback icon url
- Add-on integrity hash output to debug log if debug logging is active
- Debug mode has to be explicitly enabled in add-on config
- Translations updates

v.2.7.1
- Hot Fix: fix kids category [EU region]

v.2.7.0
- Hot Fix: new retrieve method for home lists [EU region]
- This fix avoid the "a new version of the application should be used" error message coming from HBO Go
- The additional home lists (recommendation, featured, various editor lists, ecc... are fully functional again)
- Minor fixes

v.2.6.3
- Fix minor subtitle offset (sp/no handler)
- Translations updates
- Minor fixes and optimizations

v.2.6.2
- Subtitle cache autocleaning and manual subtitle cache cleaning
- Translations updates
- Optimize plot (show only "abstract" or "description")
- Move from deprecated xbmc.translatePath to new xbmcvfs.translatePath for Kodi 19+

v.2.6.1
- Recent Kodi 19 API compatibility changes
- Swedish translation by @Sopor
- Minor changes

v.2.6.0
- Updated and improved subtitle support for Spain/Nordic region (major ttml2srt update)

v.2.5.10
- Improve elapsed time function (prevent failed report play status to Hbo in some cases)
- Alternative method to retrieve season listing (slower) in case standard one fail for some reason (happen rarely, usually its just temporary error, but the add-on can deal with it now without bothering the user)
- Translations update

v.2.5.8
- Translations update

v.2.5.7
- Option to disable device-id based credential encryption (for troubleshooting, or if problems, expert option, warning for users if disabled)

v.2.5.6
- Fix encoding problems in profile paths with unicode characters (ex. Windows username with special characters)
- Clean-up and revision of encoding problematic points (to prevent surprises in the future)

v.2.5.5
- Fix setup for operators with direct (affiliate) login. Fix setup and login for these operators: Bulgaria: Telekabel, NET1; Czech Republic: Vodafone Česká republika, Skylink CZ from 1.4.2020, UPC TV (from 1.4.2020); Montenegro: MTEL; Romania: Telekom Romania; Serbia: Test RS 1, Supernova; Slovakia: Skylink SK from 1.4.2020, Portugal: Vodafone TV, Vodafone Móvel

v.2.5.4
- Cache subtitles for the EU region if inject subtitles option is enabled (default), workaround to avoid the sometimes disappearing internal subtitles defined in the manifest

v.2.5.3
- SPDX License update
- Support for non  ascii username/password (experimental)

v.2.5.0
- Fix playing the same content twice with caching enabled for Spain/Nordic region
- Minor code/style fixes
- Update translations
- Remove pycryptodomex dependency ,use a pure python aes implementation (pyaes)
  [THIS VERSION WILL ASK TO RE-ENTER CREDENTIALS]
  [THIS IMPROVE OUT OF THE BOX COMPATIBILITY WITH MORE DEVICES, NO NOTICABLE PERFORMANCE DIFFERENCE FOR THE USE]
  [pycryptodomex had to be installed from command line on many Linux, macOS]
  
v.2.4.0
- New enhanced Kids category (EU handler)
- Legacy Kids category removed (removed from API, EU handler)
- Enhanced search too include Kids shows and movies (EU handler)
- Kids only mode (activate in settings to display only Kids category and nothing else)
  [mainly intended for use with Kodi profiles, you have to prevent changing settings with the profile where you want too enforce this]
- Search result limits fixes
- Language files fixes
- Minor fixes

v.2.3.10
- Fixed encoding error on opening search category

v.2.3.9
- Update to hr_hr translation (by @arvvoid)
- Update to hu_hu translation (by @Ajnasz)
- Update to es_es translation (by @boblo1)
- Update to ro_ro translation (by @tmihai20)
- Update to fi_fi translation (by @jumakki)
- Minor fixes

v.2.3.7
- Update to hr_hr translation (by @arvvoid)
- Update to hu_hu translation (by @Ajnasz)
- Update to es_es translation (by @boblo1)
- Update to ro_ro translation (by @tmihai20)
- Update to fi_fi translation (by @jumakki)

v.2.3.6
- Update to es_es translation (by @boblo1)

v.2.3.5
- If not currently available, show available from date and time in the plot
- BUGFIX: Correct available from date and time
- Detect not available content before attempt play (show dialog when the content will be available)
- On playback start long inactivity error, silently re-login and retry playback automatically

v.2.3.0
- Request caching                           
- Optimize re-login on unauthorized
- Local SQlight database
- Search history
- external add-ons can search now (ability to create TMDB Helper Player)
- improved search

v.2.2.0
- duoble new line fix in ttml2srt on some subtitles
- Translations update
- Set content type for listings based on the media type of the majority of the items in the list
- Option to force generic "video" media type for listings

v.2.1.5
- fix Telekom Romania (My Account) login
- new logo
- fix some encoding errors on log
- better error handling on communication errors
- media info optimizations

v.2.1.1
- Prepare for Kodi official repository

v.2.1.0
- Language files updates
- Option to ignore Kodi watched status if Get Hbo Go Watched status is enabled
- Report playstatus back to Hbo Go (EU only)
- Fix UPC CZ and SK
- Fix UPC Romania
- Use Video as media type
- Start screen customization
- History (EU only option)
- Continue watching (only display the category, EU only option)
- Fix Skylink CZ and SK (contribution ferdabasek)

v.2.0.22
- Nordic/Spain: Add Watchlist (My List)
- Nordic/Spain: Add search function
- Nordic/Spain: Add/Remove to/from My List
- Code Optimizations

v.2.0.20
- THIS IS A STABLE RELEASE
- Eu Handler: use api v8

v.2.0.19-beta38
- THIS IS A RELEASE CANDIDATE VERSION
- Fix failed del session bug
- Use urlencode to create urls (contribution Ajnasz)
- Fix uuid encoding on some systems

v.2.0.18-beta37
- THIS IS A RELEASE CANDIDATE VERSION
- Compatibility fixes Python 2/3

v.2.0.17-beta34
- THIS IS A RELEASE CANDIDATE VERSION
- SECURITY: make use of defusedxml
- SECURITY: removed pickle, implemented alternative more secure method for storing the session
- Code style fixes
- add-on passing all kodi-addon-checker tests
- moved widevine check/setup to initial step of add-on setup
- update to Hungarian translation (contribution Ajnasz)

v.2.0.16-beta33
- Removed unnecessary data from debug log (full loggin can be enabled from options if necessary)
- Added support for Kodi 19 Matrix (ALPHA)/Python3 (have to install defusedxml manually in Kodi)
- Check for widevine and setup widevine during setup
- Gracefully fail on missing cryptodome
- Changed get device unique identifier for credential encryption (used code from @CastagnaIT Netflix add-on)

v.2.0.15-beta32
- Lowered inputstream.adaptive requirement

v.2.0.15-beta31
- Better exception handling (easier debug)
- Simplify and fix minute counting in ms to SRT conversion (contribution yuppity)

v.2.0.14-beta30
- Add support for italics in subtitles [Hbo Nordic/Spain] (contribution Paco8)

v.2.0.13-beta29
- updated dependencies
- minor fixes
- better integration with inputstream.helper
- improvements to Hungarian translation (contribution mrthosi)

v.2.0.12-beta28
- updated dependencies
- fix listing limit for Hbo Nordic/Spain

v.2.0.11-beta27
- ttml2srt: add support for timestamp format in seconds (contribution of awdAvenger).

v.2.0.10-beta26
- Removed silent register api (removed on hbo go side)
- Initial individualization and device id get generated client side.

v.2.0.9-beta25
- Added Czech translation by Ike201

v.2.0.9-beta24
- Added Romanian translation by tmihai20

v.2.0.9-beta23
- HBO Spain+Nordic basic support (Spain, Norway, Denmark, Sweden, Finland)

v.2.0.8-beta22
- Enhanced media info

v.2.0.7-beta21
- Fix device ID if characters outside of ASCII are present

v.2.0.7-beta20
- Kids category and weekly top (might not be present for all countries)

v.2.0.7-beta19
- Credentials are no longer stored in cleartext and are encrypted using a calculated key from hardware info (this is not to be considered secure if your device is compromised the credentials should be considered compromised)
- Refresh session timer on reloading session

v.2.0.6-beta18
- Polish language added (contribution of kowalmisiek).
- Language files ID range fix

v.2.0.6-beta17
- Add to My List
- Remove from My List
- Rate Movies and TV Shows
- If OAuth unexpectedly fail for Operators with login redirection the add-on won't crash but display an informative message and write data that can help fix it to the debug log.

v.2.0.5-beta16
- Fixed a bug that prevented some countries from completing setup.
- Bumped inputstream.adaptive requirement to 2.3.15

v.2.0.5-beta15
- Minor fix.

v.2.0.5-beta14
- More robust categories listings. Solves #11 Portugal.

v.2.0.5-beta13
- Improved categories listings. Compatible with #11 Portugal.

v.2.0.4-beta12
- fix for #5 operators with login redirect (experimental need testing, please report)
- fix for #11 Portugal (experimental need testing, please report)
- bug fixes

v.2.0.3-beta11
- Fixed individualization/device storing. This bug caused needles device re-registration. (You can delete old registred devices, but don't have to do so, from your Hbo Go account, leave just the last registred one, the devices this add-on register will appear as Chrome 71 on Linux in Hbo Go)

v.2.0.3-beta10
- Country codes fix, flag api fix

v.2.0.3-beta9
- Guided user-friendly initial setup
- Code cleanup

v.2.0.2-beta8
- Added support for Portugal (web registration operators, and Vodafon TV operator)

v.2.0.1-beta7
- Minor cosmetic fixes
        
v.2.0.1-beta6
- Complete rewrite and restructure of the add-on (missed errors might be present, testing welcome)
- More robust login
- Persistent session
- Navigation improvemnts
- Correct views/media types (watched status shown)
- Structured to support multiple regions in the future, for now only http://hbogo.eu (covers 12 countries) is implemented

v.2.0-beta5
- Code cleaning
- Additional settings
- WORK IN PROGRESS: Translations

v.2.0-beta4
- Persistent session

v.2.0-beta3
- Code cleaning
- More info in debug log
- Option to force original movie/episode names
- EXPERT OPTION: Show episode/movie names in scraper friendly format (useful only for some external library integration addons)

v.2.0-beta2
- More info in debug log
- Providers using redirection login are identified (preparation for implementation of that login method)

v.2.0-beta1
- Added support for all hbogo.eu: Bosnia and Herzegovina, Bulgaria, Croatia, Czech Republic, Hungary, Macedonia, Montenegro, Polonia, Romania, Serbia, Slovakia, Slovenija
- Minor bugfixes

v.1.3.1.EU
- Minor bugfixes

v.1.3.EU
- Language of retrived HBO Go Eu content is set from currently loaded language file

v.1.2.EU
- Added support for Hungary

v.1.1.EU
- First General HBO Go Eu Realease
- Added support for Croatia
