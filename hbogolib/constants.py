# encoding: utf-8
# hbo constants
# Copyright (C) 2019 ArvVoid (https://github.com/arvvoid)
# Relesed under GPL version 2
#########################################################

class HbogoConstants(object):

    #supported countrys:
    #   0 name
    #   1 national domain
    #   2 country code short
    #   3 country code long
    #   4 default language code
    #   5 special domain
    #   6 hbogo region/handler to use

    HANDLER_EU = 0
    HANDLER_NORDIC = 1
    HANDLER_SPAIN = 1
    HANDLER_US = 2
    HANDLER_LATIN_AMERICA = 3
    HANDLER_ASIA = 4

    countries = [
        ['Bosnia and Herzegovina', 'ba', 'ba', 'BIH', 'HRV', '', HANDLER_EU],
        ['Bulgaria', 'bg', 'bg', 'BGR', 'BUL', '', HANDLER_EU],
        ['Croatia', 'hr', 'hr', 'HRV', 'HRV', '', HANDLER_EU],
        ['Czech Republic', 'cz', 'cz', 'CZE', 'CES', '', HANDLER_EU],
        ['Hungary', 'hu', 'hu', 'HUN', 'HUN', '', HANDLER_EU],
        ['Macedonia', 'mk', 'mk', 'MKD', 'MKD', '', HANDLER_EU],
        ['Montenegro', 'me', 'me', 'MNE', 'SRP', '', HANDLER_EU],
        ['Polonia', 'pl', 'pl', 'POL', 'POL', '', HANDLER_EU],
        ['Portugal', 'pt', 'pt', 'PRT', 'POR', 'https://hboportugal.com', HANDLER_EU],
        ['Romania', 'ro', 'ro', 'ROU', 'RON', '', HANDLER_EU],
        ['Serbia', 'rs', 'sr', 'SRB', 'SRP', '', HANDLER_EU],
        ['Slovakia', 'sk', 'sk', 'SVK', 'SLO', '', HANDLER_EU],
        ['Slovenija', 'si', 'si', 'SVN', 'SLV', '', HANDLER_EU],
    ]

    platforms = {

        1: "ANTA",
        2: "ANTV",
        3: "APMO",
        4: "APTA",
        5: "APTV",
        6: "BRMO",
        7: "BRTA",
        8: "CHBR",
        9: "COMP",
        10: "COTV",
        11: "CSAT",
        12: "DASH",
        13: "EDBR",
        14: "FFBR",
        15: "GOCT",
        16: "IEBR",
        17: "LGNC",
        18: "LGWO",
        19: "MOBI",
        20: "PLS3",
        21: "PLS4",
        22: "PS4P",
        23: "PLSP",
        24: "SABR",
        25: "SAOR",
        26: "SATI",
        27: "SERV",
        28: "SETX",
        29: "SFBR",
        30: "TABL",
        31: "TVHI",
        32: "TVLO",
        33: "XBOX",
        34: "XONE",

    }

    # 1 - operator website login form url, 2 - username field name, 3 - password field name, 4 form payload

    eu_redirect_login = {
        'c55e69f0-2471-46a9-a8b7-24dac54e6eb9': [None, None, None, None],  # Czech Republic: Skylink + Slovakia: Skylink
        'f0e09ddb-1286-4ade-bb30-99bf1ade7cff': [None, None, None, None],  # Czech Republic: UPC CZ + Slovakia: UPC CZ
        '414847a0-635c-4587-8076-079e3aa96035': ['https://icok.cyfrowypolsat.pl/logowanie.cp', 'j_username', 'j_password', {"j_username": None, "j_password": None, "loginFormM_SUBMIT": "1", "sInBtn": "", "javax.faces.ViewState": ""}],  # Polonia: Cyfrowy Polsat
        '972706fe-094c-4ea5-ae98-e8c5d907f6a2': [None, None, None, None],  # Romania: Telekom Romania
        '41a660dc-ee15-4125-8e92-cdb8c2602c5d': [None, None, None, None],  # Romania: UPC Romania
        '6826b525-04dc-4bb9-ada5-0a8e80a9f55a': [None, None, None, None],  # Romania: Vodafone Romania 4GTV+
    }

    eu_nick_instead_of_mail = [
        'c5ff7517-8ef8-4346-86c7-0fb328848671',  # Polonia: UPC
    ]




