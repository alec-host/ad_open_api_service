#!usr/bin/ python3
'''
@author: alec
@name: airduka extended platform
@year: 2023
'''
import os
import inspect
from typing import Optional
from fastapi_utils.cbv import cbv
from fastapi import APIRouter,Depends,Body,HTTPException,Security
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from fastapi_jwt_auth.auth_jwt import AuthJWT

import inventory_sample
from inventory_schema import CreateInventory

inventory_router = APIRouter()

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
from auth import AppAuthHeader
auth_header = AppAuthHeader('Authorization','Your_API_Key','The key should be preceeded by the word "Bearer" ie: <b style="color:green">Bearer</b> <small><kbd>Your_API_Key</kbd></small>')

@cbv(inventory_router)
class CreateInventory:
    #-.create inventory.
    @inventory_router.post("/v1/create-inventory",response_model=CreateInventory)
    async def create_inventory(self,product_info:CreateInventory=Body(example=jsonable_encoder(inventory_sample.EXAMPLE)),Authorize:AuthJWT=Depends(),token:Optional[str]=Security(auth_header.get_header())):
        """
        Add a product onto the inventory (stock).
        """
        Authorize.jwt_required()
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
