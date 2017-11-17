# HBO GO Kodi plugin

Egyszeru, megis nagyszeru kodi plugin, amivel HBO GO tartalmat lehet nezni. Fontos, HBO GO elofizetes kell hozzá!

A plugin kb 90%-ban bolgar kollegak munkaja: https://kodibg.org/forum/thread-504.html

Koszi morefire-nak az operatorid-kat.

Fuggosegek:
 * Kodi 18 (Inputstream Adaptive miatt)
 * widevinecdm

Tesztelt, mukodo szolgaltatok:
 * HBO GO webes regsztracio
 * Telenor MyTV (koszi norbi)
 * Telekom (koszi zodera)
 * UPC Direct (koszi ekrisztian)
 * UPC Magyarorszag (Sanchez997)
 
Meg nem tesztelt, de a pluginban benne levo szolgaltatok:
 * DIGI
 * INVITEL
 * Celldomolki Kabeltelevizio Kft.
 * Eurocable - Hello Digital
 * HFC-Network Kft.
 * HIR-SAT 2000 Kft.
 * Jurop Telekom
 * Kabelszat 2002
 * Klapka Lakasszovetkezet
 * Lat-Sat Kft.
 * MinDig TV Extra
 * PARISAT
 * PR-TELECOM
 * TARR Kft
 * Vac Varosi Kabeltelevizio Kft.
 * Vidanet Zrt.
 * HBO Development Hungary
 * HBO GO Vip/Club Hungary



## Kodi 18 @ LibreELEC

Ha LibreELEC-et hasznalunk, akkor tudunk frissiteni a test buildekre, amikben mar benne van a megfelelo verzioju Kodi, a megfelelő pluginnal.

Teszt buildek: https://forum.kodi.tv/showthread.php?tid=298461

Annyi a dolgod hogy a legfrissebb verziot letoltod, es a `Update` nevu shared folderbe berakod, vagy ha ssh-tol nem rettensz vissza, akkor a `/storage/.update`folderbe lewgeteled.

Ezek utan ujra kell inditani az eszkozt, es a LibreELEC frissiteni fogja magat.

## Inputstream Adaptive plugin 

Alapertelmezetten ki van kapcsolva, de az addonok kozott mar megtalalod, kapcsodl be.


## widevinecdm

DRM dll/so fajl a lejatszáshoz kell. LibreELEC eseten ennyi csak a dolgunk:

```
curl -Ls http://nmacleod.com/public/libreelec/getwidevine.sh | bash
```

Windowson ha mar van Chrome fent, akkor eleg innen kimasolni:
`c:\Program Files (x86)\Google\Chrome\Application\62.0.3202.94\WidevineCdm\_platform_specific\win_x64\`

A kulonbozo platformokhoz ide kell tenni a dll/so fajlt:

 * Linux:  libwidevinecdm.so -> `~/.kodi/cmd`

 * Windows: widevinecdm.dll -> `%APPDATA%\kodi\cdm`

 * MacOS / OS X: libwidevinecdm.dylib `~/Library/Application Support/Kodi/cdm`


## Letoltes

https://github.com/billsuxx/plugin.video.hbogohu/releases

## Kapcsolat

 * Twitter: https://twitter.com/billsuxx
 * Beszelgessunk: https://prohardver.hu/tema/kodi_xbmc_kiegeszito_magyar_nyelvu_online_filmekhe/friss.html