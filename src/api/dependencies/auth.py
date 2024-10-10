from core.security import (
    Token,
    TokenData,
    User,
    create_access_token,
    get_current_user,
    verify_password,
    get_user,
    get_password_hash
)
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def authenticate_user(username: str, password: str):
    user = await get_user(username)
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user

async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def create_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return Token(access_token=access_token, token_type="bearer")

# ... rest of the code remains unchanged ...
