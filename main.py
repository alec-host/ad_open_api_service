#!usr/bin/ python3
'''
@author: alec
@name: airduka extended platform
@year: 2023
'''
import os

from pathlib import Path
from typing import Optional

from fastapi import FastAPI,Depends,Request,Body,HTTPException
from pydantic import BaseModel
from fastapi.responses import JSONResponse,RedirectResponse
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth.auth_jwt import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException


from datetime import datetime, timedelta
import config

#from config import AppEnv

description = """
In order to get started with AiDuka Public API, you will need to first ... 🚀
"""
app = FastAPI(
    title="AiDuka Public API",
    description=description,
    version="1.0.0",
    terms_of_service="#",
    contact={
        "name": "Tech Team @",
        "url": "https://shop.airduka.com/",
        "email": "developers@airduka.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
)

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
appenv = config.AppEnv()
print(jsonable_encoder(appenv))

class Settings(BaseModel):
    authjwt_secret_key: str = SECRET_KEY

# callback to get your configuration
@AuthJWT.load_config
def get_config():
    return Settings()

class UserModel(BaseModel):
    username: str
    password: str

class GenerateToken(UserModel):
     class Config:
        schema_extra = {
			"example": {
                            "error": False,
                            "data": {
                                        "type":"bearer",
                                        "access_token":"kyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiO9.eyJzdWIiOiJ0ZXN0IiwiaWF0IjoxNjc3NjU4WzcyLCJuYmYiOjE2Nzc2NTgzNzIsImp0aSI6IjAzM2Q5NmE5LThlNjAtNGY1Zi05NjV2LTgzZGYwNDQzNGY5ZiIsImV4cCI6MTY3NzY1ODQzMiwidHlwZSI6ImFjY2VzcyIsImZyZXNoIjpmYWxzZX0.FsH5fjrm3DoU526vBqlyoiJRmKjn8mc6Qnd9vln-Adx"
                                    },
                            "message": "Token generated successfully"  
			            }
		}

class BaseProduct(BaseModel):
	product_title: str
	product_price: float
	product_description: str
	product_qty: Optional[int] = 1
	product_moq: Optional[int] = 1
	company_reference_number: str
	image_url: Optional[str] | None = None
	video_url: Optional[str] | None = None 

class BaseInventory(BaseModel):
    product_reference_number: str
    product_qty: Optional[int] = 1
    product_moq: Optional[int] = 1   
    company_reference_number: str
    branch_gps_coordinates: str
    stock_expiry_date: Optional[datetime] = None    
	
class CreateProduct(BaseProduct):
	class Config:
		schema_extra = {
			"example": {
                            "error": False,
                            "data": {
                                    "product_title":"Blue fountain Ink",
                                    "product_price":355.00,
                                    "product_description":"Just another awesome product stocked on AiDuka.",
                                    "product_reference_number": "XCEDFRGEWZ",
                                    "product_qty":1,
                                    "product_moq":1,
                                    "company_reference_number":"1234567890",
                                    "image_url":"https://",
                                    "video_url":"https://"
                                    },
                            "message": "The product has been created successfully"  
			            }
		}

class CreateInventory(BaseInventory):
    class Config:
        schema_extra = {
			"example": {
                            "error": False,
                            "data": {
                                    "product_reference_number": "XCEDFRGEWZ",
                                    "product_qty":1,
                                    "product_moq":1,
                                    "company_reference_number":"1234567890",
                                    "branch_gps_coordinates":"x,y",
                                    "stock_expiry_date":"2023-02-22 00:00:10"
                                    },
                            "message": "The product has been added onto the inventory successfully"  
			            }
		}

class ModifyProduct(BaseModel):
    data: Optional[BaseProduct]
    class Config:
        schema_extra = {
			"example": {
                            "error": False,
                            "data": {
                                    "product_title":"Blue fountain Ink",
                                    "product_price":355.00,
                                    "product_description":"Just another awesome product stocked on AiDuka.",
                                    "product_reference_number": "XCEDFRGEWZ",
                                    "product_qty":1,
                                    "product_moq":1,
                                    "company_reference_number":"1234567890",
                                    "image_url":"https://",
                                    "video_url":"https://"
                                    },
                            "message": "Product has been modified successfully"  
			            }
		}

class GetProduct(BaseModel):
	error: Optional[bool]
	data: Optional[CreateProduct]
	message: Optional[str]
    
	class Config:
		schema_extra = {
			"example": {
                            "error": False,
                            "data": {
                                    "product_title":"Blue fountain Ink",
                                    "product_price":355.00,
                                    "product_description":"Just another awesome product stocked on AiDuka.",
                                    "product_reference_number": "XCEDFRGEWZ",
                                    "product_qty":1,
                                    "product_moq":1,
                                    "company_reference_number":"1234567890",
                                    "image_url":"https://",
                                    "video_url":"https://"
                                    },
                            "message": "The product has been retrieved successfully"  
			            }
		}

product_request_example = {
                            "product_title": "Blue fountain Ink",
                            "product_price": 355.00,
                            "product_description": "Just another awesome product stocked on AiDuka.",
                            "product_qty": 1,
                            "product_moq": 1,
                            "company_reference_number": "1234567890",
                            "image_url": "https://",
                            "video_url": "https://"
                           }    

modified_product_request_example = {
                                    "product_title": "Blue fountain Ink",
                                    "product_price": 355.00,
                                    "product_description": "Just another awesome product stocked on AiDuka.",
                                    "product_qty": 1,
                                    "product_moq": 1,
                                    "image_url": "https://",
                                    "video_url": "https://"
                                   }  

stock_product_request_example = {
                                "product_reference_number": "XCEDFRGEWZ",
                                "product_qty": 1,
                                "product_moq": 1,
                                "company_reference_number": "1234567890",
                                "branch_gps_coordinates": "x,y",
                                "stock_expiry_date": "2023-02-22 00:00:00" 
                                }

token_example = {
                "username":"string",
                "password":"string"
                }

@app.get("/",include_in_schema=False)
async def valid_get():
    return JSONResponse(
        status_code=404,
        content={"error":True,"message": "Method not found"},
    )

@app.post("/",include_in_schema=False)
async def valid_post():
    return JSONResponse(
        status_code=404,
        content={"error":True,"message": "Method not found"},
    )

@app.put("/",include_in_schema=False)
async def valid_put():
    return JSONResponse(
        status_code=404,
        content={"error":True,"message": "Method not found"},
    )

@app.patch("/",include_in_schema=False)
async def valid_patch():
    return JSONResponse(
        status_code=404,
        content={"error":True,"message": "Method not found"},
    )

@app.delete("/",include_in_schema=False)
async def valid_delete():
    return JSONResponse(
        status_code=404,
        content={"error":True,"message": "Method not found"},
    )

@app.head("/",include_in_schema=False)
async def valid_delete():
    return JSONResponse(
        status_code=404,
        content={"error":True,"message": "Method not found"},
    )

@app.options("/",include_in_schema=False)
async def valid_delete():
    return JSONResponse(
        status_code=404,
        content={"error":True,"message": "Method not found"},
    )

@app.post("/token",response_model=GenerateToken)
async def get_token(token_info:GenerateToken=Body(example=jsonable_encoder(token_example)),Authorize: AuthJWT=Depends()):
    """
    Generate an access token.
    """
    try:
        if token_info.username != "test" or token_info.password != "test":
            return JSONResponse(
                status_code=401,
                content={"error":True,"message":"Unauthorised user"})
        # subject identifier for who this token is for example id or username from database
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = Authorize.create_access_token(subject=token_info.username,expires_time=access_token_expires,algorithm=ALGORITHM)
        #refresh_token = Authorize.create_refresh_token(subject=user.username)
        return JSONResponse(
             status_code=200,
             content={"error":False,"data":{"type":"bearer","access_token":access_token},"message":"Token generated successfully"})
    except Exception as ex:
         raise HTTPException(**ex.__dict__)

@app.post("/createProduct",response_model=CreateProduct)
async def create_product(product_info:CreateProduct=Body(example=jsonable_encoder(product_request_example)),Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    """
	Create a new product.
    """
    try:
        data = {"product_title":product_info.product_title,"product_price":product_info.product_price}
        return JSONResponse(
			status_code=201,
			content={"error":False,"data":data,"message": "Product has been created successfully"})
    except Exception as ex:
         raise HTTPException(**ex.__dict__)

@app.get("/getProduct/{product_id}",response_model=GetProduct)
async def get_product(product_id: str):
    """
    Get details about a product which includes: product_id, product_title, product_price et al.
    """
    if(product_id is None):
        return JSONResponse(
            status_code=404,
            content=jsonable_encoder({"error":False,"data":[],"message":"Product not found"}))
    else:
        return {"error":False,"data":product_request_example,"message":"Product has been retrieved successfully"}

@app.patch("/ModifyProduct/{product_reference_number}/{company_reference_number}",response_model=ModifyProduct)
async def modify_product(product_reference_number:str,company_reference_number:str,modified_product_info:ModifyProduct=Body(example=jsonable_encoder(modified_product_request_example))):
    """
    Modify a product.
    """
    if(product_reference_number is None or company_reference_number is None):
         return JSONResponse(
              status_code=404,
              content=jsonable_encoder({"error":True,"data":[],"message":"Either product_reference_number | company_reference_number is invalid"})
         )
    data=jsonable_encoder(modified_product_request_example)
    print(data['product_title'])
    return JSONResponse(
        status_code=200,
        content=jsonable_encoder({"error":False,"data":{"product_title":data['product_title'],
                                                        "product_price":data['product_price'],
                                                        "product_description":data['product_description'],
                                                        "product_qty":data['product_qty'],
                                                        "product_reference_number":product_reference_number,
                                                        "product_qty":data['product_qty'],
                                                        "product_moq":data['product_moq'],
                                                        "company_reference_number":company_reference_number,
                                                        "image_url":data['image_url'],
                                                        "video_url":data['video_url']},"message":"Product has been modified successfully"})
    )

@app.post("/createInventory",response_model=CreateInventory)
async def create_inventory(product_info: CreateInventory=Body(example=jsonable_encoder(stock_product_request_example))):
    """
    Add a product onto the inventory.
    """
    try:
        data = {
                "product_reference_number":product_info.product_reference_number,
                "product_qty":product_info.product_qty,
                "product_moq":product_info.product_moq,
                "company_reference_number":product_info.company_reference_number,
                "branch_gps_coordinate":product_info.branch_gps_coordinates,
                "stock_expiry_date":jsonable_encoder(product_info.stock_expiry_date)
               }
        return JSONResponse(
			status_code=200,
			content={"error":False,"data":data,"message":"The product has been added onto the inventory successfully"},
		)
    except Exception as ex:
        raise HTTPException(**ex.__dict__)


@app.get('/protected', operation_id="authorize")
def protected(Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()

    current_user = Authorize.get_jwt_subject()
    return {"user": current_user}


@app.exception_handler(ValueError)
async def value_error_exception_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=400,
        content=jsonable_encoder({"error":True,"message": str(exc)}),
    )

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, exc):
    return RedirectResponse("/")

# exception handler for authjwt
# in production, you can tweak performance using orjson response
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error":True,"message": exc.message}
    )