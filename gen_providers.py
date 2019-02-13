#!/usr/bin/python


# simple utility script to generate provider list for all Hbo Go Eu in a copy/pastable format
# it will generate the provider map to paste in addon.py, the list of providers for settings.xml
# and a list for readme.md
# V1.3  -- include redirect login data, check type and special hosts

import requests
import os

#country name 0 , domain 1 , shrot code 2, long code 3, lang 4, 5 special host
countries = [
    ['Bosnia and Herzegovina', 'ba', 'ba', 'BIH', 'HRV', ''],
    ['Bulgaria', 'bg', 'bg', 'BGR', 'BUL', ''],
    ['Croatia', 'hr', 'hr', 'HRV', 'HRV', ''],
    ['Czech Republic', 'cz', 'cz', 'CZE', 'CES', ''],
    ['Hungary', 'hu', 'hu', 'HUN', 'HUN', ''],
    ['Macedonia', 'mk', 'mk', 'MKD', 'MKD', ''],
    ['Montenegro', 'me', 'me', 'MNE', 'SRP', ''],
    ['Polonia', 'pl', 'pl', 'POL', 'POL', ''],
    ['Portugal', 'pt', 'pt', 'PRT', 'POR', 'https://hboportugal.com'],
    ['Romania', 'ro', 'ro', 'ROU', 'RON', ''],
    ['Serbia', 'rs', 'sr', 'SRB', 'SRP', ''],
    ['Slovakia', 'sk', 'sk', 'SVK', 'SLO', ''],
    ['Slovenija', 'si', 'si', 'SVN', 'SLV', ''],
]

# oerator name: [ OPERATOR ID, OPERATOR DOMAIN END, OPERATOR COUNTRY CODE, OPERATOR COUNTRY CODE LONG, DEFAULT LANGUAGE, IS DIRECT WEB REGISTRATION, LOGIN REDIRECTION URL]

web_operators = "   'N/A': ['00000000-0000-0000-0000-000000000000', 'hr', 'hr', 'HRV', 'ENG', True, '', 'hbogo.eu','']," + os.linesep
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
        if operator['Type'] == "D2_C":  #is web operator
            print('WEB REGISTRATION: ' + operator['Name'])
            web_operators = web_operators + "   '" + operator['Name'] + "': ['" + operator['Id'] + "', '" + countrie[1] + "', '" + countrie[2] + "', '" + countrie[3] + "', '" + countrie[4] + "', True, '', 'hbogo.eu', '" + countrie[5] + "'],"+os.linesep
            settings_string = settings_string + operator['Name'] + "|"
            info_string = info_string + "   * " + operator['Name'] + os.linesep
        else:  # is probably afiliate
            print(countrie[0] + ': ' + operator['Name'])
            extra_operators = extra_operators + "   '" + countrie[0] + ": " + operator['Name'] + "': ['" + operator['Id'] + "', '" + countrie[1] + "', '" + countrie[2] + "', '" + countrie[3] + "', '" + countrie[4] + "', False, '', 'hbogo.eu', '" + countrie[5] + "']," + os.linesep
            settings_string_operators = settings_string_operators + countrie[0] + ': ' + operator['Name'] + "|"
            info_string = info_string + "   * " + countrie[0] + ': ' + operator['Name']
            info_string = info_string + os.linesep
    json_operators = requests.get(url_operators).json()
    for operator in json_operators['Items']:
        print(countrie[0]+': '+operator['Name'])
        extra_operators = extra_operators + "   '"+countrie[0]+": "+operator['Name']+"': ['"+operator['Id']+"', '"+countrie[1]+"', '"+countrie[2]+"', '"+countrie[3]+"', '"+countrie[4]+"', False, '"+operator['RedirectionUrl']+"', 'hbogo.eu', '" + countrie[5] + "'],"+os.linesep
        settings_string_operators = settings_string_operators + countrie[0]+': '+operator['Name'] + "|"
        info_string = info_string + "   * " + countrie[0] + ': ' + operator['Name']
        if len(operator['RedirectionUrl']) > 0:
            info_string = info_string + " [REDIRECT LOGIN]"
        info_string = info_string + os.linesep

print("")
print("Preparing output...")
settings_string = settings_string + settings_string_operators
web_operators = web_operators + extra_operators

web_operators = "op_ids = {" + os.linesep + web_operators + os.linesep + "}"

output = web_operators + os.linesep + os.linesep + settings_string + os.linesep + os.linesep + info_string + os.linesep + os.linesep

print("Writing to operators.md...")
file = open("operators.md", "w")
file.write(output)
file.close()
print("Done!")