#!/usr/bin/python


# simple utility script to generate provider list for all Hbo Go Eu in a copy/pastable format
# it will generate the provider map to paste in addon.py, the list of providers for settings.xml
# and a list for readme.md

import requests
import os

#country name 0 , domain 1 , shrot code 2, long code 3, lang 4
countries = [
    ['Bosnia and Herzegovina', 'ba', 'ba', 'BIH', 'HRV'],
    ['Bulgaria', 'bg', 'bg', 'BGR', 'BUL'],
    ['Croatia', 'hr', 'hr', 'HRV', 'HRV'],
    ['Czech Republic', 'cz', 'cz', 'CZE', 'CES'],
    ['Hungary', 'hu', 'hu', 'HUN', 'HUN'],
    ['Macedonia', 'mk', 'mk', 'MKD', 'MKD'],
    ['Montenegro', 'me', 'me', 'MNE', 'SRP'],
    ['Polonia', 'pl', 'pl', 'POL', 'POL'],
    ['Romania', 'ro', 'ro', 'ROU', 'RON'],
    ['Serbia', 'rs', 'sr', 'SRB', 'SRP'],
    ['Slovakia', 'sk', 'sk', 'SVK', 'SLO'],
    ['Slovenija', 'si', 'si', 'SVN', 'SLV'],
]

web_operators = "   'N/A': ['00000000-0000-0000-0000-000000000000', 'hr', 'HRV', 'ENG', '00000000-0000-0000-0000-000000000000', True]," + os.linesep
extra_operators = ""
settings_string = ""
settings_string_operators = ""
info_string = ""
print('HBO Go Eu Operator retriver V1.0: ')
print('')
print('')
for countrie in countries:
    url_basic = 'https://api.ugw.hbogo.eu/v3.0/Operators/'+countrie[3]+'/JSON/'+countrie[4]+'/COMP'
    url_operators = 'https://'+countrie[2]+'gwapi.hbogo.eu/v2.1/Operators/json/'+countrie[3]+'/COMP'
    print('Processing operators for: '+countrie[0]+'...')
    info_string = info_string + os.linesep
    info_string = info_string + "* "+countrie[0]+os.linesep
    json_web_operators = requests.get(url_basic).json()
    for operator in json_web_operators['Items']:
        print('WEB REGISTRATION: ' + operator['Name'])
        web_operators = web_operators + "   'WEB REGISTRATION: " + operator['Name'] + "': ['" + operator['Id'] + "', '" + countrie[1] + "', '" + countrie[2] + "', '" + countrie[3] + "', '" + countrie[4] + "', True],"+os.linesep
        settings_string = settings_string + 'WEB REGISTRATION: ' + operator['Name'] + "|"
        info_string = info_string + "   * " + 'WEB REGISTRATION: ' + operator['Name'] + os.linesep
    json_operators = requests.get(url_operators).json()
    for operator in json_operators['Items']:
        print(countrie[0]+': '+operator['Name'])
        extra_operators = extra_operators + "   '"+countrie[0]+": "+operator['Name']+"': ['"+operator['Id']+"', '"+countrie[1]+"', '"+countrie[2]+"', '"+countrie[3]+"', '"+countrie[4]+"', False],"+os.linesep
        settings_string_operators = settings_string_operators + countrie[0]+': '+operator['Name'] + "|"
        info_string = info_string + "   * " + countrie[0] + ': ' + operator['Name'] + os.linesep

print("")
print("Preparing output...")
settings_string = settings_string + settings_string_operators
web_operators = web_operators + extra_operators

web_operators = "op_ids = {" + os.linesep + web_operators + os.linesep + "}"

output = web_operators + os.linesep + os.linesep + settings_string + os.linesep + os.linesep + info_string + os.linesep + os.linesep

print("Writing to operators.txt...")
file = open("operators.txt", "w")
file.write(output)
file.close()
print("Done!")