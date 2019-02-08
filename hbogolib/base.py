# encoding: utf-8
# base handler class for hbogo Kodi add-on
# Copyright (C) 2019 ArvVoid (https://github.com/arvvoid)
# Relesed under GPL version 2
#########################################################

import urllib

from hbogolib.handlereu import HbogoHandler_eu

try:
    import urllib.parse as parse
except ImportError:
    import urlparse as parse

import sys
import xbmcaddon
import xbmcgui

class hbogo(object):
    op_ids = {
        'N/A': ['00000000-0000-0000-0000-000000000000', 'hr', 'hr', 'HRV', 'ENG', True, '', 'hbogo.eu'],
        'HBO Bosnia and Herzegovina': ['6e0fe238-3b45-4049-9206-fb46425c486f', 'ba', 'ba', 'BIH', 'HRV', True, '',
                                       'hbogo.eu'],
        'HBO Bulgaria': ['b52fda48-25b2-4623-af6b-e8e30ae7d645', 'bg', 'bg', 'BGR', 'BUL', True, '', 'hbogo.eu'],
        'HBO Croatia': ['24a5e09c-4550-4cd3-a63c-8f6ab0508dd7', 'hr', 'hr', 'HRV', 'HRV', True, '', 'hbogo.eu'],
        'HBO Czech Republic': ['e04b20c2-be50-4b65-9b77-9e17e854de32', 'cz', 'cz', 'CZE', 'CES', True, '', 'hbogo.eu'],
        'HBO Hungary': ['15276cb7-7f53-432a-8ed5-a32038614bbf', 'hu', 'hu', 'HUN', 'HUN', True, '', 'hbogo.eu'],
        'HBO Macedonia': ['9b09ff6b-d2a8-48a5-84c3-31bf52add9ff', 'mk', 'mk', 'MKD', 'MKD', True, '', 'hbogo.eu'],
        'HBO Montenegro': ['54d370dd-2e28-4661-9ad4-c919b88aac4d', 'me', 'me', 'MNE', 'SRP', True, '', 'hbogo.eu'],
        'HBO Poland': ['dbaf3435-6ee2-4a79-af13-dac5a1c550a3', 'pl', 'pl', 'POL', 'POL', True, '', 'hbogo.eu'],
        'HBO Romania': ['febb7b91-f968-4a6b-8592-564f0207ab2d', 'ro', 'ro', 'ROU', 'RON', True, '', 'hbogo.eu'],
        'HBO Serbia': ['3782faaf-a461-4a4f-95ea-9b2fbcbf1958', 'rs', 'sr', 'SRB', 'SRP', True, '', 'hbogo.eu'],
        'HBO Slovakia': ['55f359e0-6038-4653-a7db-e2101da2b7a8', 'sk', 'sk', 'SVK', 'SLO', True, '', 'hbogo.eu'],
        'HBO Slovenia': ['e5ca4913-c5b8-4b08-96a3-b71abafb08aa', 'si', 'si', 'SVN', 'SLV', True, '', 'hbogo.eu'],
        'Bosnia and Herzegovina: HBO Development Bosnia': ['b461cb49-d6ad-4375-ae8b-f8dc1a97d027', 'ba', 'ba', 'BIH',
                                                           'HRV', False, '', 'hbogo.eu'],
        'Bosnia and Herzegovina: HBO GO VIP/Club Bosnia': ['926d5484-bf6f-4b2b-b20b-8f40b71f8c9a', 'ba', 'ba', 'BIH',
                                                           'HRV', False, '', 'hbogo.eu'],
        'Bosnia and Herzegovina: Telemach': ['ad36b8ac-7cd0-4f28-a57b-1ad0f44a5ec3', 'ba', 'ba', 'BIH', 'HRV', False,
                                             '', 'hbogo.eu'],
        'Bosnia and Herzegovina: Telrad Net': ['33b6e3da-83f7-438e-be0c-7a1fa6ea6197', 'ba', 'ba', 'BIH', 'HRV', False,
                                               '', 'hbogo.eu'],
        'Bulgaria: A1': ['29c994ca-48bc-4b19-a0e7-44a25b51b241', 'bg', 'bg', 'BGR', 'BUL', False, '', 'hbogo.eu'],
        'Bulgaria: M SAT CABLE EAD': ['c5afc2d3-e50d-4ddf-bd66-d1c256cca142', 'bg', 'bg', 'BGR', 'BUL', False, '',
                                      'hbogo.eu'],
        'Bulgaria: N3': ['0b17bfc7-c6a3-457f-b3fa-76547606799f', 'bg', 'bg', 'BGR', 'BUL', False, '', 'hbogo.eu'],
        'Bulgaria: NET1': ['63cc0033-1f0d-40ad-bdca-d074dbac5e73', 'bg', 'bg', 'BGR', 'BUL', False, '', 'hbogo.eu'],
        'Bulgaria: NetSurf': ['553c40d9-cf30-4a47-9051-cc7ac832e124', 'bg', 'bg', 'BGR', 'BUL', False, '', 'hbogo.eu'],
        'Bulgaria: NetWorx': ['105cc484-80a2-4710-9b1c-6f73107bf58b', 'bg', 'bg', 'BGR', 'BUL', False, '', 'hbogo.eu'],
        'Bulgaria: Silistra TV - Силистра ТВ': ['e8382e76-c870-4023-b099-4a9e5497175f', 'bg', 'bg', 'BGR', 'BUL', False,
                                                '', 'hbogo.eu'],
        'Bulgaria: Telekabel': ['4381c076-4942-43d2-8aa0-a1ab919aaf89', 'bg', 'bg', 'BGR', 'BUL', False, '',
                                'hbogo.eu'],
        'Bulgaria: Telenor': ['8d9d817a-aea5-4d9c-bf32-07ba91d66560', 'bg', 'bg', 'BGR', 'BUL', False, '', 'hbogo.eu'],
        'Bulgaria: Telenor Promo': ['7d1d3d8a-f052-402a-a964-415da5da6aec', 'bg', 'bg', 'BGR', 'BUL', False, '',
                                    'hbogo.eu'],
        'Bulgaria: Vivacom': ['60d4a508-dcc8-4d49-aacd-af9f4dc82a99', 'bg', 'bg', 'BGR', 'BUL', False, '', 'hbogo.eu'],
        'Croatia: A1': ['e1fb87d0-7581-4671-94bb-8e647e13385a', 'hr', 'hr', 'HRV', 'HRV', False, '', 'hbogo.eu'],
        'Croatia: bonbon': ['81a65859-145b-4bbc-afa6-04e9ade004f9', 'hr', 'hr', 'HRV', 'HRV', False, '', 'hbogo.eu'],
        'Croatia: evotv': ['beed025d-06c9-4cac-a8a4-a118bdf22861', 'hr', 'hr', 'HRV', 'HRV', False, '', 'hbogo.eu'],
        'Croatia: HBO GO Vip/Club Croatia': ['323f061a-34e9-4453-987b-99aa38c46480', 'hr', 'hr', 'HRV', 'HRV', False,
                                             '', 'hbogo.eu'],
        'Croatia: Hrvatski Telekom d.d.': ['73893614-eae3-4435-ab53-1d46c7f90498', 'hr', 'hr', 'HRV', 'HRV', False, '',
                                           'hbogo.eu'],
        'Croatia: Iskon Internet d.d.': ['5bff83d2-9163-4d85-9ae1-b6c2a6eabf71', 'hr', 'hr', 'HRV', 'HRV', False, '',
                                         'hbogo.eu'],
        'Croatia: Optima Telekom d.d.': ['a9e06fc5-c8d3-4b79-a776-b78d86729843', 'hr', 'hr', 'HRV', 'HRV', False, '',
                                         'hbogo.eu'],
        'Croatia: Simpa': ['3a1bb01c-9f7b-4029-a98d-6d17708fa4db', 'hr', 'hr', 'HRV', 'HRV', False, '', 'hbogo.eu'],
        'Czech Republic: freeSAT Česká republika': ['f8e915f5-4641-47b1-a585-d93f61bbbfd3', 'cz', 'cz', 'CZE', 'CES',
                                                    False, '', 'hbogo.eu'],
        'Czech Republic: Skylink': ['c55e69f0-2471-46a9-a8b7-24dac54e6eb9', 'cz', 'cz', 'CZE', 'CES', False,
                                    'https://czapi.hbogo.eu/oauthskylink/protocolgateway.aspx?caller={caller}&cid={cid}&oid=c55e69f0-2471-46a9-a8b7-24dac54e6eb9&platform=COMP&backuri={backuri}',
                                    'hbogo.eu'],
        'Czech Republic: UPC CZ': ['f0e09ddb-1286-4ade-bb30-99bf1ade7cff', 'cz', 'cz', 'CZE', 'CES', False,
                                   'https://czapi.hbogo.eu/oauthupc/protocolgateway.aspx?caller={caller}&cid={cid}&oid=f0e09ddb-1286-4ade-bb30-99bf1ade7cff&platform=COMP&backuri={backuri}',
                                   'hbogo.eu'],
        'Czech Republic: Slovak Telekom': ['3a2f741b-bcbc-455f-b5f8-cfc55fc910a3', 'cz', 'cz', 'CZE', 'CES', False, '',
                                           'hbogo.eu'],
        'Czech Republic: Lepší.TV': ['5696ea41-2087-46f9-9f69-874f407f8103', 'cz', 'cz', 'CZE', 'CES', False, '',
                                     'hbogo.eu'],
        'Czech Republic: O2': ['b8a2181d-b70a-49a7-b823-105c995199a2', 'cz', 'cz', 'CZE', 'CES', False, '', 'hbogo.eu'],
        'Czech Republic: RIO Media': ['a72f9a11-edc8-4c0e-84d4-17247c1111f5', 'cz', 'cz', 'CZE', 'CES', False, '',
                                      'hbogo.eu'],
        'Czech Republic: UPC BROADBAND SLOVAKIA': ['249309a7-6e61-436d-aa12-eeaddcfeb72e', 'cz', 'cz', 'CZE', 'CES',
                                                   False, '', 'hbogo.eu'],
        'Czech Republic: AIM': ['cdb7396a-bd2c-45e9-a023-71441e8dae64', 'cz', 'cz', 'CZE', 'CES', False, '',
                                'hbogo.eu'],
        'Czech Republic: T-Mobile Czech Republic a.s.': ['ac49b07c-4605-409c-83bd-16b5404b16a7', 'cz', 'cz', 'CZE',
                                                         'CES', False, '', 'hbogo.eu'],
        'Czech Republic: Antik Telecom': ['ad5a1855-1abd-4aa5-a947-f9942a08ca75', 'cz', 'cz', 'CZE', 'CES', False, '',
                                          'hbogo.eu'],
        'Czech Republic: CentroNet, a. s.': ['80c3f17b-718c-4f1b-9a58-67b5ac13b6fd', 'cz', 'cz', 'CZE', 'CES', False,
                                             '', 'hbogo.eu'],
        'Czech Republic: DIGI CZ s. r. o.': ['b132e3a1-ea76-4659-8656-1aac32bccd56', 'cz', 'cz', 'CZE', 'CES', False,
                                             '', 'hbogo.eu'],
        'Czech Republic: DIGI SLOVAKIA s.r.o.': ['cd2b4592-90be-4ad7-96a0-54e34ee74866', 'cz', 'cz', 'CZE', 'CES',
                                                 False, '', 'hbogo.eu'],
        'Czech Republic: FixPro': ['6c9e2104-83dc-48fb-a44c-ee3b8d689005', 'cz', 'cz', 'CZE', 'CES', False, '',
                                   'hbogo.eu'],
        'Czech Republic: flexiTV': ['1bfb5785-446d-4ca7-b7a4-cc76f48c97fe', 'cz', 'cz', 'CZE', 'CES', False, '',
                                    'hbogo.eu'],
        'Czech Republic: freeSAT Slovensko': ['b3ce9ab2-af8f-4e02-8ab7-9a01d587a35f', 'cz', 'cz', 'CZE', 'CES', False,
                                              '', 'hbogo.eu'],
        'Czech Republic: GRAPE SC': ['25e0270f-ae80-49b1-9a20-bfa47b7690e1', 'cz', 'cz', 'CZE', 'CES', False, '',
                                     'hbogo.eu'],
        'Czech Republic: HD Kabel': ['82811c4a-ad87-4bda-a1bd-2f4a4215eac4', 'cz', 'cz', 'CZE', 'CES', False, '',
                                     'hbogo.eu'],
        'Czech Republic: Kuki': ['aa2a90c0-292c-444e-a069-1ae961fa59f7', 'cz', 'cz', 'CZE', 'CES', False, '',
                                 'hbogo.eu'],
        'Czech Republic: MARTICO': ['95a5f7c8-95b7-4978-8fff-abe023249196', 'cz', 'cz', 'CZE', 'CES', False, '',
                                    'hbogo.eu'],
        'Czech Republic: Nej.cz': ['6925e9ca-9d97-446c-b3c2-09971f441f2a', 'cz', 'cz', 'CZE', 'CES', False, '',
                                   'hbogo.eu'],
        'Czech Republic: NETBOX': ['a2edba6f-bffb-4efe-bb7a-3b51e2fc0573', 'cz', 'cz', 'CZE', 'CES', False, '',
                                   'hbogo.eu'],
        'Czech Republic: Satro': ['939ffed6-d015-427e-a2f7-a82d1b846eb7', 'cz', 'cz', 'CZE', 'CES', False, '',
                                  'hbogo.eu'],
        'Czech Republic: SATT': ['064a6c6a-0556-4ff1-8d4d-c8cf3141131a', 'cz', 'cz', 'CZE', 'CES', False, '',
                                 'hbogo.eu'],
        'Czech Republic: SELFNET': ['c2c2fdb7-8562-4b16-a09c-f7530ce2ce78', 'cz', 'cz', 'CZE', 'CES', False, '',
                                    'hbogo.eu'],
        'Czech Republic: sledovanitv.cz s.r.o.': ['980a4419-1336-4056-a561-268afe7907f3', 'cz', 'cz', 'CZE', 'CES',
                                                  False, '', 'hbogo.eu'],
        'Czech Republic: Slovanet a.s.': ['8a312c76-9e9c-42e4-b38c-c0adbd6c6a93', 'cz', 'cz', 'CZE', 'CES', False, '',
                                          'hbogo.eu'],
        'Czech Republic: SWAN, a. s.': ['5b8544f8-784a-473b-97ad-159a2f95d0fb', 'cz', 'cz', 'CZE', 'CES', False, '',
                                        'hbogo.eu'],
        'Czech Republic: Tesatel': ['69253de6-3935-4c48-9557-5a1e930f30de', 'cz', 'cz', 'CZE', 'CES', False, '',
                                    'hbogo.eu'],
        'Czech Republic: HBO GO special': ['b59ee559-45b9-46a0-a40c-7f41ab6e53e9', 'cz', 'cz', 'CZE', 'CES', False, '',
                                           'hbogo.eu'],
        'Czech Republic: HBO GO Vip/Club Czech Republic': ['a215610d-aecb-4357-934f-403813a7566c', 'cz', 'cz', 'CZE',
                                                           'CES', False, '', 'hbogo.eu'],
        'Czech Republic: HBO Development Czech': ['ad729e98-c792-4bce-9588-106f11ce3b90', 'cz', 'cz', 'CZE', 'CES',
                                                  False, '', 'hbogo.eu'],
        'Czech Republic: HBO GO VIP/Club Slovakia': ['2e61999a-1b77-4ed2-b531-081dfdd3bee0', 'cz', 'cz', 'CZE', 'CES',
                                                     False, '', 'hbogo.eu'],
        'Hungary: DIGI': ['b7728684-13d5-46d9-a9a4-97d676cdaeec', 'hu', 'hu', 'HUN', 'HUN', False, '', 'hbogo.eu'],
        'Hungary: Magyar Telekom Nyrt.': ['04459649-8a90-46f1-9390-0cd5b1958a5d', 'hu', 'hu', 'HUN', 'HUN', False, '',
                                          'hbogo.eu'],
        'Hungary: Telenor MyTV': ['e71fabae-66b6-4972-9823-8743f8fcf06f', 'hu', 'hu', 'HUN', 'HUN', False, '',
                                  'hbogo.eu'],
        'Hungary: UPC Direct': ['48f48c5b-e9e4-4fca-833b-2fa26fb1ad22', 'hu', 'hu', 'HUN', 'HUN', False, '',
                                'hbogo.eu'],
        'Hungary: UPC Magyarország': ['1ca45800-464a-4e9c-8f15-8d822ad7d8a1', 'hu', 'hu', 'HUN', 'HUN', False, '',
                                      'hbogo.eu'],
        'Hungary: INVITEL': ['f2230905-8e25-4245-80f9-fccf67a24005', 'hu', 'hu', 'HUN', 'HUN', False, '', 'hbogo.eu'],
        'Hungary: Celldömölki Kábeltelevízió Kft.': ['383cd446-06fb-4a59-8d39-200a3e9bcf6f', 'hu', 'hu', 'HUN', 'HUN',
                                                     False, '', 'hbogo.eu'],
        'Hungary: Eurocable – Hello Digital': ['fe106c75-293b-42e6-b211-c7446835b548', 'hu', 'hu', 'HUN', 'HUN', False,
                                               '', 'hbogo.eu'],
        'Hungary: Flip': ['1680a41e-a9bc-499f-aca6-db1a59703566', 'hu', 'hu', 'HUN', 'HUN', False, '', 'hbogo.eu'],
        'Hungary: HFC-Network Kft.': ['42677aa5-7576-4dc7-9004-347b279e4e5d', 'hu', 'hu', 'HUN', 'HUN', False, '',
                                      'hbogo.eu'],
        'Hungary: HIR-SAT 2000 Kft.': ['3a3cce31-fb19-470a-9bb5-6947c4ac9996', 'hu', 'hu', 'HUN', 'HUN', False, '',
                                       'hbogo.eu'],
        'Hungary: JuPiNet': ['93bdad56-6fc7-4494-be0f-3660ce3752f0', 'hu', 'hu', 'HUN', 'HUN', False, '', 'hbogo.eu'],
        'Hungary: Kabelszat 2002': ['d91341c2-3542-40d4-adab-40b644798327', 'hu', 'hu', 'HUN', 'HUN', False, '',
                                    'hbogo.eu'],
        'Hungary: Klapka Lakásszövetkezet': ['18fb0ff5-9cfa-4042-be00-638c5d34e553', 'hu', 'hu', 'HUN', 'HUN', False,
                                             '', 'hbogo.eu'],
        'Hungary: Lát-Sat Kft.': ['97cddb59-79e3-4090-be03-89a6ae06f5ec', 'hu', 'hu', 'HUN', 'HUN', False, '',
                                  'hbogo.eu'],
        'Hungary: Micro-Wave kft.': ['c071ab5e-8884-434a-9702-084882c2b541', 'hu', 'hu', 'HUN', 'HUN', False, '',
                                     'hbogo.eu'],
        'Hungary: MinDig TV Extra': ['c48c350f-a9db-4eb6-97a6-9b659e2db47f', 'hu', 'hu', 'HUN', 'HUN', False, '',
                                     'hbogo.eu'],
        'Hungary: PARISAT': ['7982d5c7-63df-431d-806e-54f98fdfa36a', 'hu', 'hu', 'HUN', 'HUN', False, '', 'hbogo.eu'],
        'Hungary: PR-TELECOM': ['18f536a3-ecac-42f1-91f1-2bbc3e6cfe81', 'hu', 'hu', 'HUN', 'HUN', False, '',
                                'hbogo.eu'],
        'Hungary: TARR Kft': ['adb99277-3899-439e-8bdf-c749c90493cd', 'hu', 'hu', 'HUN', 'HUN', False, '', 'hbogo.eu'],
        'Hungary: Vác Városi Kábeltelevízió Kft.': ['5729f013-f01d-4cc3-b048-fe5c91c64296', 'hu', 'hu', 'HUN', 'HUN',
                                                    False, '', 'hbogo.eu'],
        'Hungary: Vidanet Zrt.': ['b4f422f7-5424-4116-b72d-7cede85ead4e', 'hu', 'hu', 'HUN', 'HUN', False, '',
                                  'hbogo.eu'],
        'Hungary: HBO Development Hungary': ['6a52efe0-54c4-4197-8c55-86ee7a63cd04', 'hu', 'hu', 'HUN', 'HUN', False,
                                             '', 'hbogo.eu'],
        'Hungary: HBO GO Vip/Club Hungary': ['f320aa2c-e40e-49c2-8cdd-1ebef2ac6f26', 'hu', 'hu', 'HUN', 'HUN', False,
                                             '', 'hbogo.eu'],
        'Macedonia: HBO GO Vip/Club Macedonia': ['b848c6b6-31f1-467d-9814-0011252b4b32', 'mk', 'mk', 'MKD', 'MKD',
                                                 False, '', 'hbogo.eu'],
        'Macedonia: Македонски Телеком': ['f4c9c5de-4c4b-42f4-8355-fd43bf6df571', 'mk', 'mk', 'MKD', 'MKD', False, '',
                                          'hbogo.eu'],
        'Macedonia: оне.Вип': ['2cda834c-24ef-4b21-abff-94379f770877', 'mk', 'mk', 'MKD', 'MKD', False, '', 'hbogo.eu'],
        'Montenegro: Crnogorski Telekom': ['849f94ec-96be-4520-8c0d-b0d7aadd278b', 'me', 'me', 'MNE', 'SRP', False, '',
                                           'hbogo.eu'],
        'Montenegro: HBO GO VIP/Club Montenegro': ['dcda4868-9de9-4be2-8822-1eb510af61d8', 'me', 'me', 'MNE', 'SRP',
                                                   False, '', 'hbogo.eu'],
        'Montenegro: Telemach': ['c1932a89-2060-4c00-8567-9c96e8217491', 'me', 'me', 'MNE', 'SRP', False, '',
                                 'hbogo.eu'],
        'Montenegro: Telenor': ['e52cea52-eb14-4bed-b746-eced9a1d2b7b', 'me', 'me', 'MNE', 'SRP', False, '',
                                'hbogo.eu'],
        'Polonia: Cyfrowy Polsat': ['414847a0-635c-4587-8076-079e3aa96035', 'pl', 'pl', 'POL', 'POL', False,
                                    'https://cyfrowyauth.hbogo.eu/oauth/protocolgateway.aspx?caller={caller}&cid={cid}&oid=414847a0-635c-4587-8076-079e3aa96035&platform=COMP&backuri={backuri}',
                                    'hbogo.eu'],
        'Polonia: nc+': ['07b113ce-1c12-4bfd-9823-db951a6b4e87', 'pl', 'pl', 'POL', 'POL', False, '', 'hbogo.eu'],
        'Polonia: Plus': ['a35f8cd2-05d7-4c0f-832f-0ddfad3b585d', 'pl', 'pl', 'POL', 'POL', False, '', 'hbogo.eu'],
        'Polonia: UPC': ['c5ff7517-8ef8-4346-86c7-0fb328848671', 'pl', 'pl', 'POL', 'POL', False, '', 'hbogo.eu'],
        'Polonia: Vectra': ['7021fee7-bab1-4b4b-b91c-a2dc4fdd7a05', 'pl', 'pl', 'POL', 'POL', False, '', 'hbogo.eu'],
        'Polonia: PLAY': ['22eaaeb6-1575-419f-9f1b-af797e86b9ee', 'pl', 'pl', 'POL', 'POL', False, '', 'hbogo.eu'],
        'Polonia: Multimedia Polska': ['598a984f-bc08-4e77-896b-a82d8d6ea8de', 'pl', 'pl', 'POL', 'POL', False, '',
                                       'hbogo.eu'],
        'Polonia: Netia': ['c454b13c-5c82-4a01-854f-c34b2901d1b2', 'pl', 'pl', 'POL', 'POL', False, '', 'hbogo.eu'],
        'Polonia: Orange': ['48b81f9b-cb72-48cd-85d2-e952f78137c0', 'pl', 'pl', 'POL', 'POL', False, '', 'hbogo.eu'],
        'Polonia: INEA': ['82ae5dfd-9d29-4059-a843-2aa16449c42a', 'pl', 'pl', 'POL', 'POL', False, '', 'hbogo.eu'],
        'Polonia: TOYA': ['357890f0-2698-445b-8712-b82f715b0648', 'pl', 'pl', 'POL', 'POL', False, '', 'hbogo.eu'],
        'Polonia: JAMBOX': ['5eb57ea8-9cd7-4bbf-8c6c-e56b186dd5c0', 'pl', 'pl', 'POL', 'POL', False, '', 'hbogo.eu'],
        'Polonia: PROMAX': ['2e0325fa-d4b3-41eb-a9e4-0a36ee59aec5', 'pl', 'pl', 'POL', 'POL', False, '', 'hbogo.eu'],
        'Polonia: Asta-Net': ['892771be-a48c-46ab-a0d0-3f51cdc50cf2', 'pl', 'pl', 'POL', 'POL', False, '', 'hbogo.eu'],
        'Polonia: TK Chopin': ['6a47f04f-cdd6-428b-abb5-135e38a43b38', 'pl', 'pl', 'POL', 'POL', False, '', 'hbogo.eu'],
        'Polonia: ELSAT': ['36f365ac-4ca2-4e8b-9b21-14479e5fe6bb', 'pl', 'pl', 'POL', 'POL', False, '', 'hbogo.eu'],
        'Polonia: Eltronik': ['99eed640-107c-4732-81d0-59305ff6b520', 'pl', 'pl', 'POL', 'POL', False, '', 'hbogo.eu'],
        'Polonia: SatFilm': ['f7f4d300-23ab-4b79-bb35-49568eb7cd4a', 'pl', 'pl', 'POL', 'POL', False, '', 'hbogo.eu'],
        'Polonia: Master': ['5893f3c1-0bcd-4ae3-b434-45666925b5d1', 'pl', 'pl', 'POL', 'POL', False, '', 'hbogo.eu'],
        'Polonia: STANSAT': ['8f34fcd8-3b74-4c16-b91c-c8375ab3ffdb', 'pl', 'pl', 'POL', 'POL', False, '', 'hbogo.eu'],
        'Polonia: Dialog': ['878e69aa-be98-4a7d-a08e-b11c7330d8b3', 'pl', 'pl', 'POL', 'POL', False, '', 'hbogo.eu'],
        'Polonia: Internetia': ['b49a6c5d-033d-4bf1-b273-37ba188aef97', 'pl', 'pl', 'POL', 'POL', False, '',
                                'hbogo.eu'],
        'Polonia: Petrotel': ['62f7b31b-c866-4ff3-a7a1-800fac10de16', 'pl', 'pl', 'POL', 'POL', False, '', 'hbogo.eu'],
        'Polonia: Cinema City – promocja': ['1366289b-86ae-4695-8d4b-a6b14eacdd8b', 'pl', 'pl', 'POL', 'POL', False, '',
                                            'hbogo.eu'],
        'Polonia: Samsung - promocja': ['64d88671-b490-44b9-b1ee-e145347732b3', 'pl', 'pl', 'POL', 'POL', False, '',
                                        'hbogo.eu'],
        'Polonia: Player+': ['57332e2f-958c-4a83-86cc-e569842868a2', 'pl', 'pl', 'POL', 'POL', False, '', 'hbogo.eu'],
        'Polonia: Test operator': ['ec6276ae-2246-41c1-b0a9-ed06daa385ce', 'pl', 'pl', 'POL', 'POL', False, '',
                                   'hbogo.eu'],
        'Polonia: HBO GO Vip/Club Poland': ['b7018ed3-1858-4436-8e7f-d92a6d0b9bfc', 'pl', 'pl', 'POL', 'POL', False, '',
                                            'hbogo.eu'],
        'Romania: AKTA': ['defb1446-0d52-454c-8c86-e03715f723a8', 'ro', 'ro', 'ROU', 'RON', False, '', 'hbogo.eu'],
        'Romania: Canal S': ['381ba411-3927-4616-9c6a-b247d3ce55e8', 'ro', 'ro', 'ROU', 'RON', False, '', 'hbogo.eu'],
        'Romania: HBO GO Vip/Club Romania': ['4949006b-8112-4c09-87ad-18d6f7bfee02', 'ro', 'ro', 'ROU', 'RON', False,
                                             '', 'hbogo.eu'],
        'Romania: INES': ['0539b12f-670e-49ff-9b09-9cef382e4dae', 'ro', 'ro', 'ROU', 'RON', False, '', 'hbogo.eu'],
        'Romania: INTERSAT': ['078a922e-df7c-4f34-a8de-842dea7f4342', 'ro', 'ro', 'ROU', 'RON', False, '', 'hbogo.eu'],
        'Romania: Metropolitan': ['cb71c5a8-9f21-427a-a37e-f08abf9605be', 'ro', 'ro', 'ROU', 'RON', False, '',
                                  'hbogo.eu'],
        'Romania: MITnet': ['959cf6b2-34b1-426d-9d51-adf04c0802b0', 'ro', 'ro', 'ROU', 'RON', False, '', 'hbogo.eu'],
        'Romania: NextGen Communications': ['cf66ff47-0568-485f-902d-0accc1547ced', 'ro', 'ro', 'ROU', 'RON', False, '',
                                            'hbogo.eu'],
        'Romania: Orange Romania': ['754751b7-1406-416e-b4bd-cb6566656de2', 'ro', 'ro', 'ROU', 'RON', False, '',
                                    'hbogo.eu'],
        'Romania: RCS RDS': ['c243a2f3-d54e-4365-85ad-849b6908d53e', 'ro', 'ro', 'ROU', 'RON', False, '', 'hbogo.eu'],
        'Romania: Telekom Romania': ['972706fe-094c-4ea5-ae98-e8c5d907f6a2', 'ro', 'ro', 'ROU', 'RON', False,
                                     'https://roapi.hbogo.eu/oauthromtelekom/protocolgateway.aspx?caller={caller}&cid={cid}&oid=972706fe-094c-4ea5-ae98-e8c5d907f6a2&platform=COMP&backuri={backuri}',
                                     'hbogo.eu'],
        'Romania: Telekom Romania Business': ['6baa4a6e-d707-42b2-9a79-8b475c125d86', 'ro', 'ro', 'ROU', 'RON', False,
                                              '', 'hbogo.eu'],
        'Romania: TV SAT 2002': ['d68c2237-1f3f-457e-a708-e8e200173b8d', 'ro', 'ro', 'ROU', 'RON', False, '',
                                 'hbogo.eu'],
        'Romania: UPC Romania': ['41a660dc-ee15-4125-8e92-cdb8c2602c5d', 'ro', 'ro', 'ROU', 'RON', False,
                                 'https://roapi.hbogo.eu/oauthupcrom/protocolgateway.aspx?caller={caller}&cid={cid}&oid=41a660dc-ee15-4125-8e92-cdb8c2602c5d&platform=COMP&backuri={backuri}',
                                 'hbogo.eu'],
        'Romania: Vodafone': ['92e30168-4ca6-4512-967d-b79e584a22b6', 'ro', 'ro', 'ROU', 'RON', False, '', 'hbogo.eu'],
        'Romania: Vodafone Romania 4GTV+': ['6826b525-04dc-4bb9-ada5-0a8e80a9f55a', 'ro', 'ro', 'ROU', 'RON', False,
                                            'https://roapi.hbogo.eu/oauthvodafone/protocolgateway.aspx?caller={caller}&cid={cid}&oid=6826b525-04dc-4bb9-ada5-0a8e80a9f55a&platform=COMP&backuri={backuri}',
                                            'hbogo.eu'],
        'Romania: Voucher HBOGO': ['da5a4764-a001-4dac-8e52-59d0ae531a62', 'ro', 'ro', 'ROU', 'RON', False, '',
                                   'hbogo.eu'],
        'Serbia: HBO GO Promo (rs)': ['6b63c0fe-91a6-41e8-ac8a-9a214834f697', 'rs', 'sr', 'SRB', 'SRP', False, '',
                                      'hbogo.eu'],
        'Serbia: HBO GO Vip/Club Serbia': ['f3b52ca0-ea89-4f1d-91eb-02a4f7f60e7d', 'rs', 'sr', 'SRB', 'SRP', False, '',
                                           'hbogo.eu'],
        'Serbia: SAT-TRAKT': ['486efd34-38ee-4ed5-86c0-a96f8ab09f2a', 'rs', 'sr', 'SRB', 'SRP', False, '', 'hbogo.eu'],
        'Serbia: SBB': ['54bfd03b-a4a3-43a3-87da-9a41d67b13e8', 'rs', 'sr', 'SRB', 'SRP', False, '', 'hbogo.eu'],
        'Serbia: Telekom Srbija': ['0d085ea6-63c9-452e-b5ec-db1aa8b38fef', 'rs', 'sr', 'SRB', 'SRP', False, '',
                                   'hbogo.eu'],
        'Serbia: Telenor': ['1fac38e7-3677-4607-b60a-f968b80d8084', 'rs', 'sr', 'SRB', 'SRP', False, '', 'hbogo.eu'],
        'Slovakia: freeSAT Česká republika': ['f8e915f5-4641-47b1-a585-d93f61bbbfd3', 'sk', 'sk', 'SVK', 'SLO', False,
                                              '', 'hbogo.eu'],
        'Slovakia: Skylink': ['c55e69f0-2471-46a9-a8b7-24dac54e6eb9', 'sk', 'sk', 'SVK', 'SLO', False,
                              'https://czapi.hbogo.eu/oauthskylink/protocolgateway.aspx?caller={caller}&cid={cid}&oid=c55e69f0-2471-46a9-a8b7-24dac54e6eb9&platform=COMP&backuri={backuri}',
                              'hbogo.eu'],
        'Slovakia: UPC CZ': ['f0e09ddb-1286-4ade-bb30-99bf1ade7cff', 'sk', 'sk', 'SVK', 'SLO', False,
                             'https://czapi.hbogo.eu/oauthupc/protocolgateway.aspx?caller={caller}&cid={cid}&oid=f0e09ddb-1286-4ade-bb30-99bf1ade7cff&platform=COMP&backuri={backuri}',
                             'hbogo.eu'],
        'Slovakia: Slovak Telekom': ['3a2f741b-bcbc-455f-b5f8-cfc55fc910a3', 'sk', 'sk', 'SVK', 'SLO', False, '',
                                     'hbogo.eu'],
        'Slovakia: Lepší.TV': ['5696ea41-2087-46f9-9f69-874f407f8103', 'sk', 'sk', 'SVK', 'SLO', False, '', 'hbogo.eu'],
        'Slovakia: O2': ['b8a2181d-b70a-49a7-b823-105c995199a2', 'sk', 'sk', 'SVK', 'SLO', False, '', 'hbogo.eu'],
        'Slovakia: RIO Media': ['a72f9a11-edc8-4c0e-84d4-17247c1111f5', 'sk', 'sk', 'SVK', 'SLO', False, '',
                                'hbogo.eu'],
        'Slovakia: UPC BROADBAND SLOVAKIA': ['249309a7-6e61-436d-aa12-eeaddcfeb72e', 'sk', 'sk', 'SVK', 'SLO', False,
                                             '', 'hbogo.eu'],
        'Slovakia: AIM': ['cdb7396a-bd2c-45e9-a023-71441e8dae64', 'sk', 'sk', 'SVK', 'SLO', False, '', 'hbogo.eu'],
        'Slovakia: T-Mobile Czech Republic a.s.': ['ac49b07c-4605-409c-83bd-16b5404b16a7', 'sk', 'sk', 'SVK', 'SLO',
                                                   False, '', 'hbogo.eu'],
        'Slovakia: Antik Telecom': ['ad5a1855-1abd-4aa5-a947-f9942a08ca75', 'sk', 'sk', 'SVK', 'SLO', False, '',
                                    'hbogo.eu'],
        'Slovakia: CentroNet, a. s.': ['80c3f17b-718c-4f1b-9a58-67b5ac13b6fd', 'sk', 'sk', 'SVK', 'SLO', False, '',
                                       'hbogo.eu'],
        'Slovakia: DIGI CZ s. r. o.': ['b132e3a1-ea76-4659-8656-1aac32bccd56', 'sk', 'sk', 'SVK', 'SLO', False, '',
                                       'hbogo.eu'],
        'Slovakia: DIGI SLOVAKIA s.r.o.': ['cd2b4592-90be-4ad7-96a0-54e34ee74866', 'sk', 'sk', 'SVK', 'SLO', False, '',
                                           'hbogo.eu'],
        'Slovakia: FixPro': ['6c9e2104-83dc-48fb-a44c-ee3b8d689005', 'sk', 'sk', 'SVK', 'SLO', False, '', 'hbogo.eu'],
        'Slovakia: flexiTV': ['1bfb5785-446d-4ca7-b7a4-cc76f48c97fe', 'sk', 'sk', 'SVK', 'SLO', False, '', 'hbogo.eu'],
        'Slovakia: freeSAT Slovensko': ['b3ce9ab2-af8f-4e02-8ab7-9a01d587a35f', 'sk', 'sk', 'SVK', 'SLO', False, '',
                                        'hbogo.eu'],
        'Slovakia: GRAPE SC': ['25e0270f-ae80-49b1-9a20-bfa47b7690e1', 'sk', 'sk', 'SVK', 'SLO', False, '', 'hbogo.eu'],
        'Slovakia: HD Kabel': ['82811c4a-ad87-4bda-a1bd-2f4a4215eac4', 'sk', 'sk', 'SVK', 'SLO', False, '', 'hbogo.eu'],
        'Slovakia: Kuki': ['aa2a90c0-292c-444e-a069-1ae961fa59f7', 'sk', 'sk', 'SVK', 'SLO', False, '', 'hbogo.eu'],
        'Slovakia: MARTICO': ['95a5f7c8-95b7-4978-8fff-abe023249196', 'sk', 'sk', 'SVK', 'SLO', False, '', 'hbogo.eu'],
        'Slovakia: Nej.cz': ['6925e9ca-9d97-446c-b3c2-09971f441f2a', 'sk', 'sk', 'SVK', 'SLO', False, '', 'hbogo.eu'],
        'Slovakia: NETBOX': ['a2edba6f-bffb-4efe-bb7a-3b51e2fc0573', 'sk', 'sk', 'SVK', 'SLO', False, '', 'hbogo.eu'],
        'Slovakia: Satro': ['939ffed6-d015-427e-a2f7-a82d1b846eb7', 'sk', 'sk', 'SVK', 'SLO', False, '', 'hbogo.eu'],
        'Slovakia: SATT': ['064a6c6a-0556-4ff1-8d4d-c8cf3141131a', 'sk', 'sk', 'SVK', 'SLO', False, '', 'hbogo.eu'],
        'Slovakia: SELFNET': ['c2c2fdb7-8562-4b16-a09c-f7530ce2ce78', 'sk', 'sk', 'SVK', 'SLO', False, '', 'hbogo.eu'],
        'Slovakia: sledovanitv.cz s.r.o.': ['980a4419-1336-4056-a561-268afe7907f3', 'sk', 'sk', 'SVK', 'SLO', False, '',
                                            'hbogo.eu'],
        'Slovakia: Slovanet a.s.': ['8a312c76-9e9c-42e4-b38c-c0adbd6c6a93', 'sk', 'sk', 'SVK', 'SLO', False, '',
                                    'hbogo.eu'],
        'Slovakia: SWAN, a. s.': ['5b8544f8-784a-473b-97ad-159a2f95d0fb', 'sk', 'sk', 'SVK', 'SLO', False, '',
                                  'hbogo.eu'],
        'Slovakia: Tesatel': ['69253de6-3935-4c48-9557-5a1e930f30de', 'sk', 'sk', 'SVK', 'SLO', False, '', 'hbogo.eu'],
        'Slovakia: HBO GO special': ['b59ee559-45b9-46a0-a40c-7f41ab6e53e9', 'sk', 'sk', 'SVK', 'SLO', False, '',
                                     'hbogo.eu'],
        'Slovakia: HBO GO Vip/Club Czech Republic': ['a215610d-aecb-4357-934f-403813a7566c', 'sk', 'sk', 'SVK', 'SLO',
                                                     False, '', 'hbogo.eu'],
        'Slovakia: HBO Development Czech': ['ad729e98-c792-4bce-9588-106f11ce3b90', 'sk', 'sk', 'SVK', 'SLO', False, '',
                                            'hbogo.eu'],
        'Slovakia: HBO GO VIP/Club Slovakia': ['2e61999a-1b77-4ed2-b531-081dfdd3bee0', 'sk', 'sk', 'SVK', 'SLO', False,
                                               '', 'hbogo.eu'],
        'Slovenija: Ario d.o.o.': ['660cd5e3-4630-4283-ad5d-50b65ebdeea8', 'si', 'si', 'SVN', 'SLV', False, '',
                                   'hbogo.eu'],
        'Slovenija: HBO GO Promo (si)': ['5d4cc09d-2947-48c0-ac65-91d52786907d', 'si', 'si', 'SVN', 'SLV', False, '',
                                         'hbogo.eu'],
        'Slovenija: HBO GO Vip/Club Slovenia': ['eb266b63-532b-4c53-bf9b-b7190d5f75db', 'si', 'si', 'SVN', 'SLV', False,
                                                '', 'hbogo.eu'],
        'Slovenija: KRS CATV Selnica-Ruše': ['f196f33a-d8ce-47b9-91b8-af8864a34dbc', 'si', 'si', 'SVN', 'SLV', False,
                                             '', 'hbogo.eu'],
        'Slovenija: T-2 d.o.o.': ['7d442a4b-1c7c-4f4d-a991-7a80ad4e9094', 'si', 'si', 'SVN', 'SLV', False, '',
                                  'hbogo.eu'],
        'Slovenija: Telekom Slovenije': ['2387fe14-c430-45f5-a23d-7c22ec5670aa', 'si', 'si', 'SVN', 'SLV', False, '',
                                         'hbogo.eu'],
        'Slovenija: Telemach': ['93a542b5-b4d8-4c76-bf3b-1eb261e39cfe', 'si', 'si', 'SVN', 'SLV', False, '',
                                'hbogo.eu'],

    }

    def __init__(self, addon_id, handle, base_url):
        self.base_url = base_url
        self.handle = handle
        self.addon_id = addon_id
        self.addon = xbmcaddon.Addon(self.addon_id)
        self.language = self.addon.getLocalizedString
        operator = self.addon.getSetting('operator')
        if operator == 'N/A':
            xbmcgui.Dialog().ok(self.language(33702).encode('utf-8'), self.language(32104).encode('utf-8'))
            xbmcaddon.Addon(id=self.addon_id).openSettings()
            sys.exit()

        try:
            self.country = self.op_ids[operator]
        except:
            xbmcgui.Dialog().ok(self.language(33702).encode('utf-8'), self.language(32104).encode('utf-8'))
            xbmcaddon.Addon(id=self.addon_id).openSettings()
            sys.exit()

        if self.country[7] == 'hbogo.eu':
            self.handler=HbogoHandler_eu(self.addon_id, self.handle, self.base_url, self.country, operator)
        else:
            xbmcgui.Dialog().ok("ERROR", "Unsupported region")
            xbmcaddon.Addon(id=self.addon_id).openSettings()
            sys.exit()

    def router(self, arguments):
        params = dict(parse.parse_qsl(arguments))

        url = None
        name = None
        thumbnail = None
        cid = None
        mode = None


        try:
            url = urllib.unquote_plus(params["url"])
        except:
            pass
        try:
            name = urllib.unquote_plus(params["name"])
        except:
            pass
        try:
            thumbnail = str(params["thumbnail"])
        except:
            pass
        try:
            mode = int(params["mode"])
        except:
            pass
        try:
            content_id = str(params["cid"])
        except:
            pass

        if mode == None or url == None or len(url) < 1:
            self.handler.categories()

        elif mode == 1:
            self.handler.setDispCat(name)
            self.handler.list(url)

        elif mode == 2:
            self.handler.setDispCat(name)
            self.handler.season(url)

        elif mode == 3:
            self.handler.setDispCat(name)
            self.handler.episode(url)

        elif mode == 4:
            self.handler.setDispCat(self.language(33711).encode('utf-8'))
            self.handler.search()

        elif mode == 5:
            self.handler.setDispCat(name)
            self.handler.play(url, content_id)





