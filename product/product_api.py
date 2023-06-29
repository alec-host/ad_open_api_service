#!usr/bin/ python3
'''
@author: alec
@name: airduka extended platform
@year: 2023
'''
import os
import inspect
import json as js
from typing import Optional,List
from fastapi_utils.cbv import cbv
from fastapi import APIRouter, Depends,Body,HTTPException,Header,Security
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from fastapi.security import APIKeyHeader

from fastapi_jwt_auth.auth_jwt import AuthJWT

import product_sample
from product_schema import CreateMultipleProduct, CreateMultipleProductResponse,CreateProduct,GetProduct,ModifyProduct

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
from auth import AppAuthHeader

auth_header = AppAuthHeader('Authorization','Your_API_Key','The key should be preceeded by the word "Bearer" ie: <b style="color:green">Bearer</b> <small><kbd>Your_API_Key</kbd></small>')

product_router = APIRouter()

@cbv(product_router)
class CreateProduct:
    #-.add a new product.
    @product_router.post("/v1/create-product",response_model=CreateProduct)
    async def create_product(self,product_info:CreateProduct=Body(example=jsonable_encoder(product_sample.CREATE_EXAMPLE)),Authorize:AuthJWT=Depends(),token:Optional[str]=Security(auth_header.get_header())):
        """
        Create a single product that belongs to an existing mechant on AirDuka shop.
        """
        Authorize.jwt_required()
        try:
            data = {"product_title":product_info.product_title,"product_price":product_info.product_price}
            return JSONResponse(
                status_code=201,
                content={"error":False,"data":data,"message": "Product has been created successfully"})
        except Exception as ex:
            raise HTTPException(**ex.__dict__)

    #-.create muiltple new products.   
    @product_router.post("/v1/create-multiple-products",response_model=CreateMultipleProduct,response_model_exclude_none=True,responses={200:{"content":{"application/json":{"example":{"error":False,"message":"The batch request has been queued successfully"}}}}})
    async def create_multiple_products(self,product_info:CreateMultipleProduct=Body(example=jsonable_encoder(product_sample.CREATE_MUILTI_EXAMPLE),media_type="application/json"),Authorize:AuthJWT=Depends(),token:Optional[str]=Security(auth_header.get_header())):
        """
        Create multiple products that belongs to an existing mechant on AirDuka shop.
        """
        Authorize.jwt_required()
        try:
            data={"error":False,"message":"The batch request has been queued successfully"}
            return JSONResponse(
                status_code=200,
                content=data)
        except Exception as ex:
            raise HTTPException(**ex.__dict__)

    #-.edit a product.
    @product_router.patch("/v1/modify-product/{product_reference_number}/{company_reference_number}",response_model=ModifyProduct)
    async def modify_product(self,product_reference_number:str,company_reference_number:str,modified_product_info:ModifyProduct=Body(example=jsonable_encoder(product_sample.MODIFY_EXAMPLE)),Authorize:AuthJWT=Depends(),token:Optional[str]=Security(auth_header.get_header())):
        """
        Modify particulars of a product.
        """
        Authorize.jwt_required()
        if(product_reference_number is None or company_reference_number is None):
            return JSONResponse(
                status_code=404,
                content=jsonable_encoder({"error":True,"data":[],"message":"Either product_reference_number | company_reference_number is invalid"}))
        data=jsonable_encoder(product_sample.MODIFY_EXAMPLE)
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
                                                            "video_url":data['video_url']},"message":"Product has been modified successfully"}))

    #-.get a product.
    @product_router.get("/v1/get-product/{product_id}",response_model=GetProduct)
    async def get_product(self,product_id: str,Authorize:AuthJWT=Depends(),token:Optional[str]=Security(auth_header.get_header())):
        """
        Get details about a product which includes: product_id, product_title, product_price et al.
        """
        Authorize.jwt_required()
        if(product_id is None):
            return JSONResponse(
                status_code=404,
                content=jsonable_encoder({"error":False,"data":[],"message":"Product not found"}))
        else:
            return JSONResponse(status_code=200,content={"error":False,"data":product_sample.CREATE_EXAMPLE,"message":"Product has been retrieved successfully"})