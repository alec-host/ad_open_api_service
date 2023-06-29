#!usr/bin/ python3
'''
@author: alec
@name: airduka extended platform
@year: 2023
'''
import sys

sys.path.insert(0,"C:/testapp/user/")
import user_schema

class GenerateToken(user_schema.UserModel):
     class Config:
        schema_extra = {
			"example": {
                            "error":False,
                            "data":{
                                "token_type":"bearer",
                                "access_token":"kyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiO9.eyJzdWIiOiJ0ZXN0IiwiaWF0IjoxNjc3NjU4WzcyLCJuYmYiOjE2Nzc2NTgzNzIsImp0aSI6IjAzM2Q5NmE5LThlNjAtNGY1Zi05NjV2LTgzZGYwNDQzNGY5ZiIsImV4cCI6MTY3NzY1ODQzMiwidHlwZSI6ImFjY2VzcyIsImZyZXNoIjpmYWxzZX0.FsH5fjrm3DoU526vBqlyoiJRmKjn8mc6Qnd9vln-Adx",
                                "expires_in":3599
                            },
                            "message":"Token generated successfully"  
			            }
		}