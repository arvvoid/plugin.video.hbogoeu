# HBO GO Kodi plugin

Egyszerű, mégis nagyszerű kodi plugin, amivel HBO GO tartalmat lehet nézni. Fontos, HBO GO előfizetős 
kell hozzá!

A plugin kb 90%-ban bolgár kollégák munkája: https://kodibg.org/forum/thread-504.html
Koszi morefire-nak az operatorid-kat.


Fuggosegek:
* Kodi 18 (Inputstream Adaptive miatt)
* widevinecdm


## Kodi 18

Ha Libreelecet használunk, akkor tudunk frissíteni a test buildekre, amikben már benne van a megfelelő verziójú Kodi, a megfelelő pluginnal.

Teszt buildek: https://forum.kodi.tv/showthread.php?tid=298461

Annyi a dolgod h a legfrisebbet letoltod, es a Update nevu shared folderbe berakod, vagy ha ssh-tol nem rettensz vissza, akkor a /storage/.update folderbe lewgeteled,

Restart (update)


## widevinecdm

DRM dll/so fajl a lejátszáshoz kell. Libreelec esetén ennyi csak a dolgunk:

```
curl -Ls http://nmacleod.com/public/libreelec/getwidevine.sh | bash
```

Más platformoknál be kell szerezni a dll/so fájlt, és a kodi/cmd könyvtár alá bemásolni.


Linux:  libwidevinecdm.so -t kell beszerezni és a ~/.kodi/cmd alá bemásolni

Windows: widevinecdm.dll -t kell beszerzni és ide másolni: %APPDATA%\kodi\cdm

MacOS / OS X: libwidevinecdm.dylib -t kell beszerezni és a  /Users/<your_user_name>/Library/Application Support/Kodi/cdm mappába másolni
