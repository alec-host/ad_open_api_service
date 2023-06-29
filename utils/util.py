#!usr/bin/ python3
'''
@author: alec
@name: airduka extended platform
@year: 2023
'''
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse,RedirectResponse
from fastapi import Request

class HttpUtils:
    def custom_request_handler(request,composed_json):
            app_route = None
            route_arr = None
            print("xx")
            #-.which route method is served?
            if(request.method == "POST"):
                app_route = request.scope['path']
            elif(request.method == "GET"):
                route_arr = str(request.scope['path']).split("/")
                app_route = "/"+route_arr[1]+"/"+route_arr[2]+"/{product_id}"
            else:
                route_arr = str(request.scope['path']).split("/")
                app_route = "/"+route_arr[1]+"/"+route_arr[2]+"/{product_reference_number}/{company_reference_number}"

            if(route_arr is not None):
                #-.check of app route exists.
                if(any(sd['path'] == str(app_route) for sd in composed_json['data']) == False):   
                        return RedirectResponse("/")
                else:
                    if(int(len(route_arr)) == 4 and str(route_arr[3]) == "" and request.method == "GET" or (int(len(route_arr)) > 4 and request.method == "GET")):
                        return RedirectResponse("/")
                    elif(int(len(route_arr)) == 4 and str(route_arr[3]) == "" and request.method == "PATCH" or (int(len(route_arr)) == 4 and str(route_arr[3]) != "" and request.method == "PATCH")):
                        return RedirectResponse("/")
                    elif(int(len(route_arr)) == 5 and str(route_arr[3]) == "" and request.method == "PATCH" or int(len(route_arr)) > 5):
                        return RedirectResponse("/")    
                    else:
                        return  JSONResponse(status_code=500,content=jsonable_encoder({"error":True,"message":"Something wrong has happened|no token provided"}))
            else:
                return  JSONResponse(status_code=500,content=jsonable_encoder({"error":True,"message":"Something wrong has happened|no token provided"}))
