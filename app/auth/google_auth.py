import os
from datetime import datetime, timedelta
from dotenv import load_dotenv

from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi.responses import RedirectResponse
from jose import jwt, JWTError
from authlib.integrations.starlette_client import OAuth

from ..repository.UserRepository import UserRepository
from ..db.database import get_db
from app.schema.UserSchema import UserCreate

# === Load environment variables ===
load_dotenv()

# === OAuth Setup ===
oauth = OAuth()
oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"},
)

# === JWT Config ===
ACCESS_TOKEN_EXPIRE_MINUTES = float(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
JWT_SECRET_KEY = os.getenv("SECRET_KEY", "supersecret")
JWT_ALGORITHM = os.getenv("ALGORITHM", "HS256")

router = APIRouter()

# === Auth Routes ===
@router.get("/login/google")
async def google_login(request: Request):
    redirect_uri = request.url_for("google_auth_callback")
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get("/callback", name="google_auth_callback")
async def google_auth_callback(request: Request, db=Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.userinfo(token=token)

    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to retrieve user info")

    user_repo = UserRepository(db)
    user = user_repo.get_by_email(user_info["email"])

    if not user:
        now = datetime.utcnow()
        user_in = UserCreate(
            name=user_info.get("name", ""),
            email=user_info["email"],
            address="",
            phone_number="",
            created_at=now,
            updated_at=now,
        )
        user = user_repo.create(user_in)

    # Generate JWT
    jwt_payload = {
        "sub": str(user.id),
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    jwt_token = jwt.encode(jwt_payload, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)

    # Set secure cookie
    response = RedirectResponse(url="/")
    response.set_cookie(
        key="access_token",
        value=jwt_token,
        httponly=True,
        secure=False,             # ✅ Set to True in production with HTTPS
        samesite="strict",       # ✅ Prevent CSRF
        max_age=int(ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    )

    return response

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie(
        key="access_token",
        httponly=True,
        secure=True,
        samesite="strict"
    )
    return response

# === Auth Dependency ===
def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
