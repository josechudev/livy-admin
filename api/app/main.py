
import fastapi
import httpx
import starlette

from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

from starlette.background import BackgroundTask

from fastapi import Depends, status, HTTPException
import os
import secrets

from fastapi import status, HTTPException
from fastapi.security import OAuth2PasswordBearer, api_key

import app.auth as auth


SERVER = "https://virtserver.swaggerhub.com/josechudev/livy/1.0.0"

app = FastAPI()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
client = httpx.AsyncClient(base_url=SERVER)


@app.get("/")
def home():
    return {"message": "Livy server"}
@app.get("/sessions")
async def get_sessions(api_key: api_key.APIKey = Depends(auth.get_api_key)):
    req = client.build_request('GET', SERVER + '/sessions')
    rp_resp = await client.send(req)
    return fastapi.responses.JSONResponse(content=rp_resp.json())

async def _reverse_proxy(request: Request):
    url = httpx.URL(path=request.url.path, query=request.url.query.encode("utf-8"))
    rp_req = client.build_request(
        request.method, url, headers=request.headers.raw, content=await request.body()
    )
    rp_resp = await client.send(rp_req)
    return fastapi.responses.JSONResponse(content=rp_resp.json())



app.add_route("/{path:path}", _reverse_proxy, ["GET", "POST"])
