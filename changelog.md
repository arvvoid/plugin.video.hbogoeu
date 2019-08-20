v.2.0.12-beta28
- updated dependencies
- fix listing limit for Hbo Nordic/Spain

v.2.0.11-beta27
- ttml2srt: add support for timestamp format in seconds.

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
