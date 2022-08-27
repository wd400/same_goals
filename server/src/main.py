
from dataclasses import MISSING
import uvicorn
import os
import os.path   
from fastapi import FastAPI, HTTPException, Depends, Request

from logs import LOGGER
from fastapi import FastAPI, File, UploadFile
from starlette.middleware.cors import CORSMiddleware



from mysql_helpers import MySQLHelper
from operations.load import do_load
from operations.search import search_in_milvus,query_search
from operations.count import do_count
from operations.drop import do_drop
from logs import LOGGER
from encode import SentenceModel
from pydantic import BaseModel
import sys
from typing import Optional

from fastapi.responses import JSONResponse
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException

print("start import")
from milvus_helpers import MilvusHelper
print("stop import")

class Settings(BaseModel):
    authjwt_secret_key: str = "focbzoejcnoendoincxs"
    authjwt_access_token_expires: int= 60*60*12
    authjwt_token_location: set = {"cookies"}
    authjwt_cookie_csrf_protect: bool = False

# in the request headers to access.
@AuthJWT.load_config
def get_config():
    return Settings()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://d3t3x9jw381f19.cloudfront.net"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"])

print("BEFORE MILVUS",file=sys.stderr)
MILVUS_CLI = MilvusHelper()
print("AFTER MILVUS")
MYSQL_CLI = MySQLHelper()

print("BEFORE MODEL")
MODEL = SentenceModel()
print("AFTER MODEL")


class User(BaseModel):
    username: str
    password: str

class Content(BaseModel):
    content: str

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@app.post('/login')
async def login(user: User, Authorize: AuthJWT = Depends() ):
    # Returns the total number of titles in the system
    try:
        if MYSQL_CLI.login(user.username, user.password):
            access_token = Authorize.create_access_token(subject=user.username)
            Authorize.set_access_cookies(access_token)
            return {'status': True, "msg":"Successfully login"}
        else:
            return {'status': False, 'msg': "wrong user/password"}
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}

@app.post('/signup')
def signup( user: User):
    try:

        if not (3<=len(user.username)<=20) or not user.username.isalnum():
            return {'status': False, 'msg': "invalid user"}

        if not (3<=len(user.password)<=20) or not user.password.isalnum():
            return {'status': False, 'msg': "invalid password"}


        if MYSQL_CLI.signup(user.username,user.password):
            return {'status': True, 'msg': ""}
        return {'status': False, 'msg': "user exists?"}
    except Exception as e:
        return {'status': False, 'msg': e}


@app.get('/logout')
def logout(Authorize: AuthJWT = Depends()):

    Authorize.jwt_required()

    Authorize.unset_jwt_cookies()
    return {"msg":"Successfully logout"}


@app.get('/delete/{id}')
async def delete(id:int, Authorize: AuthJWT = Depends()):
    # Delete the collection of Milvus and MySQL
    
    Authorize.jwt_required()
    try:
        do_drop(id,Authorize.get_jwt_subject(), MILVUS_CLI, MYSQL_CLI)
        LOGGER.info("Successfully drop tables in Milvus and MySQL!")
        return {'status': True, 'msg': ""}
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}


@app.post('/add')
async def add(todo:Content,Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    if len(todo.content)<3:
        return {'status': False, 'msg': "too small"}
    if len(todo.content)>100:
        return {'status': False, 'msg': "too long"}
    try:
        id=do_load(todo.content,Authorize.get_jwt_subject(),MODEL ,MILVUS_CLI, MYSQL_CLI)
        LOGGER.info(f"Successfully loaded data")
        return {'status': True, 'id':str(id)}
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}

@app.get('/user/{user}')
async def user(user:str):
    try:
        todos=MYSQL_CLI.user_todos(user)
        LOGGER.info(f"Successfully loaded data2")
        return {"todos":todos,'status':True}
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}

@app.get('/similar/{user}')
async def similar( user:str):
    try:
        LOGGER.info("ici_1")
        result = search_in_milvus(user, MILVUS_CLI, MYSQL_CLI)
        LOGGER.info("ici_2")
        return {'status':True, "result":result}
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}


@app.post('/search')
async def search( query:Content):
    try:
        LOGGER.info("ici_1")
        result = query_search(query.content, MODEL, MILVUS_CLI, MYSQL_CLI)
        LOGGER.info("ici_2")
        
        return {'status': True, 'result': result} 
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}

@app.get('/description/{user}')
async def get_description(user:str):
    try:
        description=MYSQL_CLI.get_description(user)
        return {"description":description}
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}

@app.post('/description')
async def modify_description(description:Content,Authorize: AuthJWT = Depends()):
    Authorize.jwt_required()
    try:
        MYSQL_CLI.update_description(Authorize.get_jwt_subject(),description.content)
        return {'status': True, 'msg': ""}
    except Exception as e:
        LOGGER.error(e)
        return {'status': False, 'msg': e}

if __name__ == "__main__":
    uvicorn.run(app=app, host='0.0.0.0', port=5000)
