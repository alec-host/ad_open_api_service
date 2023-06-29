#!usr/bin/ python3
'''
@author: alec
@name: airduka extended platform
@year: 2023
'''
import os
import sys
import inspect
import uvicorn
from fastapi import FastAPI
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse,RedirectResponse
from fastapi import FastAPI,Request
from starlette.exceptions import HTTPException as StarletteHTTPException

from fastapi_jwt_auth.exceptions import AuthJWTException

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)

sys.path.insert(0,currentdir+"/access_token/")
import token_api 

sys.path.insert(0,currentdir+"/product/")
import product_api

sys.path.insert(0,currentdir+"/inventory/")
import inventory_api

sys.path.insert(0,currentdir+"/utils/")
from message import custom_error_message,authjwt_error_message

description = """
In order to get started with AiDuka Extended Shop API, you will need to first ... 🚀

The Extended Shop API allow you to automate the process of product creation, product modification & inventory management. The API exposes the following services
<ul>
    <li><small>Create Product</small></li>
    <li><small>Create Multiple Products</small></li>
    <li><small>Modify Product</small></li>
    <li><small>Get Product</small></li>
    <li><small>Create Inventory</small></li>
</ul>

Before you begin as a prerequisite, you need to have credentials to <b>AirDuka Extended Shop API</b> account. If you don’t have one, kindly send an email request to <a href="mailto:developers@airduka.com">ad developer</a> for an account to setup.
"""
app = FastAPI(
    title="AiDuka Extended Shop API",
    description=description,
    version="1.0.0",
    terms_of_service="#",
    contact={
        "name": "AirDuka Services",
        "email": "developers@airduka.com",
        "url": "https://shop.airduka.com/",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    docs_url=None
)

@app.get("/",include_in_schema=False)
async def valid_get():
    return JSONResponse(
        status_code=404,
        content={"error":True,"message":custom_error_message()[0]['ERROR_002']},
    )

@app.post("/",include_in_schema=False)
async def valid_post():
    return JSONResponse(
        status_code=404,
        content={"error":True,"message":custom_error_message()[0]['ERROR_002']},
    )

@app.put("/",include_in_schema=False)
async def valid_put():
    return JSONResponse(
        status_code=404,
        content={"error":True,"message":custom_error_message()[0]['ERROR_002']},
    )

@app.patch("/",include_in_schema=False)
async def valid_patch():
    return JSONResponse(
        status_code=404,
        content={"error":True,"message":custom_error_message()[0]['ERROR_002']},
    )

@app.delete("/",include_in_schema=False)
async def valid_delete():
    return JSONResponse(
        status_code=404,
        content={"error":True,"message":custom_error_message()[0]['ERROR_002']},
    )

@app.head("/",include_in_schema=False)
async def valid_delete():
    return JSONResponse(
        status_code=404,
        content={"error":True,"message":custom_error_message()[0]['ERROR_002']},
    )

@app.options("/",include_in_schema=False)
async def valid_delete():
    return JSONResponse(
        status_code=404,
        content={"error":True,"message":custom_error_message()[0]['ERROR_002']},
    )

@app.get("/docs",include_in_schema=False)
async def no_docs():
    return RedirectResponse("https://shop.airduka.com")

app.include_router(token_api.access_token_router,tags=["TOKEN"])
app.include_router(product_api.product_router,tags=["PRODUCT"])
app.include_router(inventory_api.inventory_router,tags=["INVENTORY"])

@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"error":True,"message": str(exc)}),
    )

#-.Custom error handler.
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: ValueError):
    app_route = None
    route_arr = None
    #-.get all the app's route.
    url_list = [
        {"path":route.path,"name":route.name}
        for route in request.app.routes
    ]
    #-.re-format the json.
    composed_json = {"data":url_list}
    try:
        #-.which route method is served?
        if(request.method == "POST"):
            route_arr = str(request.scope['path'])
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
                elif((int(len(route_arr)) == 5 and str(route_arr[3]) == "" and request.method == "PATCH") or (int(len(route_arr)) > 5 and request.method == "PATCH")):
                    return RedirectResponse("/") 
                else:
                    return  JSONResponse(status_code=500,content=jsonable_encoder({"error":True,"message":custom_error_message()[0]['ERROR_001']}))
        else:
            return  JSONResponse(status_code=500,content=jsonable_encoder({"error":True,"message":custom_error_message()[0]['ERROR_001']}))
    except Exception as ex:
        return RedirectResponse("/")
    
#-.exception handler for authjwt.
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error":True,"message":str(exc.message).replace(authjwt_error_message()[0]['ERROR_001'],custom_error_message()[0]['ERROR_004']).replace(authjwt_error_message()[0]['ERROR_002'],custom_error_message()[0]['ERROR_003']).replace(authjwt_error_message()[0]['ERROR_003'],custom_error_message()[0]['ERROR_003']).replace(authjwt_error_message()[0]['ERROR_004'],custom_error_message()[0]['ERROR_003'])}
    )

if __name__ == "__main__":
    uvicorn.run("app:app",host="127.0.0.1",port=6000,reload=False,log_level="info")