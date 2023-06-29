#!usr/bin/ python3
'''
@author: alec
@name: airduka extended platform
@year: 2023
'''

import json as js
ERROR_001 = "Something wrong has happened|bearer no token provided"
ERROR_002 = "Method not found"
ERROR_003 = "Invalid Token"
ERROR_004 = "Token has expired"
ERROR_005 = ""
ERROR_006 = ""
ERROR_007 = ""
ERROR_008 = ""
ERROR_009 = ""
ERROR_010 = ""
ERROR_011 = ""
ERROR_012 = ""
ERROR_013 = ""
ERROR_014 = ""
ERROR_015 = ""

AUTH_ERROR_001 = "Signature has expired"
AUTH_ERROR_002 = "Not enough segments"
AUTH_ERROR_003 = "Invalid header padding"
AUTH_ERROR_004 = "Invalid header string: 'utf-8' codec can't decode byte 0xb2 in position 2: invalid start byte"

def custom_error_message():
    return (js.loads(js.dumps([{"ERROR_001":ERROR_001,"ERROR_002":ERROR_002,"ERROR_003":ERROR_003,"ERROR_004":ERROR_004}])))

def authjwt_error_message():
    return (js.loads(js.dumps([{"ERROR_001":AUTH_ERROR_001,"ERROR_002":AUTH_ERROR_002,"ERROR_003":AUTH_ERROR_003,"ERROR_004":AUTH_ERROR_004}])))