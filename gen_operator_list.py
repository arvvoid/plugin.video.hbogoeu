#!/usr/bin/python
# encoding: utf-8
# Copyright (C) 2019-2020 ArvVoid (https://github.com/arvvoid)
# SPDX-License-Identifier: GPL-2.0-or-later

from __future__ import absolute_import, division

#  simple utility script to generate provider list for all Hbo Go Eu
#  usefull for wiki and documentation and get the
#  "big picture" and have a panorama of all operators.
#  will generate marked-up list for documentation

import requests
import os
import codecs
from datetime import date

from hbogolib.constants import HbogoConstants

info_string = ""
print('HBO Go Eu Operator retriver V2.0: ')
print('')
print('')
for countrie in HbogoConstants.countries:
    if countrie[6] == HbogoConstants.HANDLER_EU:
        url_basic = 'https://api.ugw.hbogo.eu/v3.0/Operators/' + str(countrie[3]) + '/JSON/' + str(countrie[4]) + '/COMP'
        url_operators = 'https://' + str(countrie[2]) + 'gwapi.hbogo.eu/v2.1/Operators/json/' + str(countrie[3]) + '/COMP'
        print('Processing operators for: ' + str(countrie[0]) + '...')
        info_string = info_string + os.linesep
        info_string = info_string + "* " + str(countrie[0]) + os.linesep
        json_web_operators = requests.get(url_basic).json()
        for operator in json_web_operators['Items']:
            print('DIRECT ' + operator['Type'] + ': ' + operator['Name'])
            info_string = info_string + "   * " + 'DIRECT ' + operator['Type'] + ': ' + operator['Name'] + os.linesep
        json_operators = requests.get(url_operators).json()
        for operator in json_operators['Items']:
            strtype = "AFFILIATE: "
            if len(operator['RedirectionUrl']) > 0:
                strtype = "AFFILIATE REDIRECT LOGIN: "
            print(strtype + ': ' + operator['Name'])
            info_string = info_string + "   * " + strtype + operator['Name'] + os.linesep

print("")
print("Preparing output...")

output = "Last update: " + str(date.today()) + os.linesep + info_string + os.linesep + os.linesep

print("eu_operators.md...")
file = codecs.open("eu_operators.md", "w", "utf-8")
file.write(output)
file.close()
print("Done!")
