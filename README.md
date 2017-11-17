# HBO GO Kodi plugin

Egyszeru, megis nagyszeru kodi plugin, amivel HBO GO tartalmat lehet nezni. Fontos, HBO GO elofizetes kell hozzá!

A plugin kb 90%-ban bolgar kollegak munkaja: https://kodibg.org/forum/thread-504.html

Koszi morefire-nak az operatorid-kat.

Fuggosegek:
 * Kodi 18 (Inputstream Adaptive miatt)
 * widevinecdm

Tesztelt, mukodo szolgaltatok:
 * Telenor (koszi noribi)
 * Telekom (koszi zodera)
 * HBO GO webes regsztracio

Meg nem tesztelt, de a pluginban benne levo szolgaltatok:
 * UPC Direct
 * DIGI
 * UPC Magyarorszag
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



## Kodi 18

Ha Libreelecet hasznalunk, akkor tudunk frissíteni a test buildekre, amikben mar benne van a megfelelo verzioju Kodi, a megfelelő pluginnal.

Teszt buildek: https://forum.kodi.tv/showthread.php?tid=298461

Annyi a dolgod h a legfrissebbet letoltod, es a `Update` nevu shared folderbe berakod, vagy ha ssh-tol nem rettensz vissza, akkor a `/storage/.update`folderbe lewgeteled,

Restart (update)


## widevinecdm

DRM dll/so fajl a lejatszáshoz kell. Libreelec eseten ennyi csak a dolgunk:

```
curl -Ls http://nmacleod.com/public/libreelec/getwidevine.sh | bash
```

Mas platformokhoz is be kell szerezni a dll/so fajlt:

 * Linux:  libwidevinecdm.so -> `~/.kodi/cmd`

 * Windows: widevinecdm.dll -> `%APPDATA%\kodi\cdm`

 * MacOS / OS X: libwidevinecdm.dylib `/Users/<your_user_name>/Library/Application Support/Kodi/cdm`


## Letoltes

https://github.com/billsuxx/plugin.video.hbogohu/releases