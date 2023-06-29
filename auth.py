from fastapi.security import APIKeyHeader
from dotenv import dotenv_values

#auth_header = APIKeyHeader(name='Authorization',scheme_name='Your_API_Key',description='The key should be preceeded by the word "Bearer" ie: <b style="color:green">Bearer</b> <small><kbd>Your_API_Key</kbd></small>')
class AppAuthHeader():
    def __init__(self,name,schema_name,description):
        self.name=name
        self.schema_name=schema_name
        self.description=description
    
    def get_header(self):
        config = dotenv_values(".env")

        return APIKeyHeader(name=self.name,scheme_name=self.schema_name,description=self.description)