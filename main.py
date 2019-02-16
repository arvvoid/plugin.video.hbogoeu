# encoding: utf-8
# base handler class for hbogo Kodi add-on
# Copyright (C) 2019 ArvVoid (https://github.com/arvvoid)
# Relesed under GPL version 2
#########################################################

from hbogolib.base import hbogo
import sys
import xbmc


# Setup plugin
PLUGIN_HANDLE = int(sys.argv[1])
BASE_URL = sys.argv[0]
# We use string slicing to trim the leading ? from the plugin call paramstring
REQUEST_PARAMS = sys.argv[2][1:]

def get_addon_data():
    # Loads the Kodi plugin data from addon.xml
    root_dir = os.path.dirname(os.path.abspath(__file__))
    pathname = os.path.join(root_dir, 'addon.xml')
    with open(pathname, 'rb') as addon_xml:
        addon_xml_contents = addon_xml.read()
        _id = re.search(
            r'(?<!xml )id="(.+?)"',
            addon_xml_contents).group(1)
        author = re.search(
            r'(?<!xml )provider-name="(.+?)"',
            addon_xml_contents).group(1)
        name = re.search(
            r'(?<!xml )name="(.+?)"',
            addon_xml_contents).group(1)
        version = re.search(
            r'(?<!xml )version="(.+?)"',
            addon_xml_contents).group(1)
        return {
            'id': _id,
            'author': author,
            'name': name,
            'version': version
        }


if __name__ == '__main__':
    addon_data = get_addon_data()
    xbmc.log(addon_data['id'] + " STARING VERSION: " + addon_data['version'], xbmc.LOGDEBUG)
    addon_main = hbogo(addon_data.id, PLUGIN_HANDLE, BASE_URL)
    addon_main.router(REQUEST_PARAMS)

