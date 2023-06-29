#!usr/bin/ python3
'''
@author: alec
@name: airduka extended platform
@year: 2023
'''
from pydantic import BaseModel,Field

class UserModel(BaseModel):
    username: str = Field(default=None,title="Username",description=None)
    password: str = Field(default=None,title="Password",description=None)