#!usr/bin/ python3
'''
@author: alec
@name: airduka extended platform
@year: 2023
'''
import os
import sys
import inspect
from fastapi_utils.cbv import cbv
from fastapi import APIRouter, Depends,Body,HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from fastapi_jwt_auth.auth_jwt import AuthJWT

from datetime import timedelta

import token_sample

currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir+"/access_token/")
import settings_schema
import token_schema

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60

access_token_router = APIRouter()

#-.callback to get your configuration
@AuthJWT.load_config
def get_config():
    return settings_schema.Settings()

#-.generate a token.
@cbv(access_token_router)
class GenerateAccessToken:
    @access_token_router.post("/v1/token",response_model=token_schema.GenerateToken)
    async def generate_token(self,token_info:token_schema.GenerateToken=Body(example=jsonable_encoder(token_sample.EXAMPLE)),Authorize:AuthJWT=Depends()):
        """
        Generate an access token
        """
        try:
            if token_info.username != "test" or token_info.password != "test":
                return JSONResponse(
                    status_code=401,
                    content={"error":True,"message":"Unauthorised user"})
            #-.subject identifier for who this token is for example id or username from database
            access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = Authorize.create_access_token(subject=token_info.username,expires_time=access_token_expires,algorithm=ALGORITHM)
            #refresh_token = Authorize.create_refresh_token(subject=user.username)
            return JSONResponse(
                status_code=200,
                content={"error":False,"data":{"token_type":"bearer","access_token":access_token,"expires_in":3599},"message":"Token generated successfully"})
        except Exception as ex:
            raise HTTPException(**ex.__dict__)