# encoding: utf-8
# HBO Go EU Add-on lib Test Script
# Copyright (C) 2019 ArvVoid (https://github.com/arvvoid)
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
# Relesed under GPL version 2
#########################################################

from __future__ import absolute_import, division

import sys

if __name__ == '__main__':
    print("HBO GO EU Test Script")
    print("---------------------")

    if len(sys.argv) > 2:
        test_type = str(sys.argv[1])
        if test_type == "ttml2srt":
            from hbogolib.ttml2srt import Ttml2srt
            input_subs_path = str(sys.argv[2])
            print("Loading TTML file "+input_subs_path+" ...")
            ttml = Ttml2srt(input_subs_path, 25)
            print("Converting...")
            srt_file = ttml.write_srt_file("test_sub")
            print("SRT written to: "+srt_file)
            print("DONE!")
        elif test_type == "utils":
            from hbogolib.util import Util
            text = str(sys.argv[2])
            Result_b = Util.base64enc_bytes(text)
            Result_s = Util.base64enc_string(text)
            print("Base64 Encode Bytes: ", Result_b)
            print("Base64 Encode String: ", Result_s)
            print("Base64 Decode Bytes: ", Util.base64dec_bytes(Result_s))
            print("Base64 Decode String: ", Util.base64dec_string(Result_s))
            print("Hashing: ", Util.hash225_string(text))
            print("Hashing bytes: ", Util.hash225_bytes(text))
            print("DONE!")
        else:
            print("Ivalid test!")
    else:
        print("USAGE:")
        print("     python test.py [TEST_TYPE] [PARAM1] [PARAM2] ...")
        print("TTML2SRT Test:")
        print("     python test.py ttml2srt ttml_subs.xml")
        print("     python test.py utils text")
