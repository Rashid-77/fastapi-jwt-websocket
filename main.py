import secrets
import uvicorn

from datetime import datetime, timedelta
from typing import Any, Union

from fastapi import FastAPI, Depends, HTTPException, status
from fastapi import WebSocket, WebSocketException
from fastapi.security import APIKeyHeader
from jose import jwt, JWTError
from pydantic import ValidationError


app = FastAPI()

#-------------------------------------------------------------------------
SECRET_KEY = secrets.token_urlsafe(32)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 365 * 24 * 60

def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    if expires_delta:
        expire = datetime.utcnow() + timedelta(minutes=expires_delta)
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str):
    return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

#---------------------------------------------------------------
jwt_origin = ""

@app.get("/login")
async def login():
    '''
    pass here username and password the way you want
    check here credential
    if credential OK then create access token
    '''
    global jwt_origin

    jwt_origin = create_access_token("Vasja", expires_delta=ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": jwt_origin,
        "token_type": "bearer",
    }


#---------------------------------------------------------------
async def api_key_header(websocket: WebSocket):
    print('api_key_header()')
    api_key_header = APIKeyHeader(name="secret")
    return await api_key_header(websocket)


async def authenticate_user(api_key: str = Depends(api_key_header)):
    print('authenticate_user()')
    print(f'{api_key=}')
    if api_key != jwt_origin:
        raise HTTPException(status_code=401, detail="Ошибка аутентификации")
    print('aaa')
    return api_key


@app.websocket("/")
async def websocket_endpoint(websocket: WebSocket, token: str = Depends(authenticate_user)):
    try:
        payload = decode_access_token(token)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    except (JWTError, ValidationError):
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)

    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        await websocket.send_text(f"Authenticated user {user_id} says: {data}")


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)