#!/usr/bin/python
# encoding: utf-8
# HBO Go EU Add-on lib Test Script
# Copyright (C) 2019-2020 ArvVoid (https://github.com/arvvoid)
#
# USAGE:
#    > python test.py [TEST_TYPE] [PARAM1] [PARAM2] ...
#
#   SUBTITLES TEST
#    > python test.py ttml2srt ttml_subs.xml
#
#       OUTPUT:
#           Messages on the console
#           The test_sub.srt file will contain the result of the conversion
#
# SPDX-License-Identifier: GPL-2.0-or-later
#########################################################

from __future__ import absolute_import, division

import sys

if __name__ == '__main__':
    print("HBO GO EU Test Script")
    print("---------------------")

    if len(sys.argv) > 2:
        test_type = str(sys.argv[1])
        if test_type == "ttml2srt":
            from libs.ttml2srt import Ttml2Srt
            input_subs_path = str(sys.argv[2])
            print("Loading TTML file " + input_subs_path + " ...")
            ttml = Ttml2Srt(input_subs_path, 25)
            print("Converting...")
            srt_file = ttml.write2file(ttml.mfn2srtfn("test_sub", ttml.lang, False))
            print("DONE!")
        else:
            print("Ivalid test!")
    else:
        print("USAGE:")
        print("     python test.py [TEST_TYPE] [PARAM1] [PARAM2] ...")
        print("TTML2SRT Test:")
        print("     python test.py ttml2srt ttml_subs.xml")
