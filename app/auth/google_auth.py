from fastapi import APIRouter, Depends, Request, HTTPException
from authlib.integrations.starlette_client import OAuth
from starlette.config import Config
from starlette.responses import RedirectResponse
import os
from repository.UserRepository import UserRepository
from db.database import get_db

config = Config(".env")
oauth = OAuth(config)

oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    client_kwargs={'scope': 'openid email profile'}
)

router = APIRouter()

@router.get('/login')
async def login(request: Request):
    redirect_uri = request.url_for('auth')
    return await oauth.google.authorize_redirect(request, redirect_uri)

@router.get('/auth')
async def auth(request: Request, db=Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = await oauth.google.parse_id_token(request, token)
    if not user_info:
        raise HTTPException(status_code=400, detail="Failed to retrieve user info")

    user_repo = UserRepository(db)
    user = user_repo.get_by_email(user_info["email"])
    if not user:
        # You can extend UserCreate to accept Google info
        from app.schema.UserSchema import UserCreate
        user_in = UserCreate(
            name=user_info.get("name", ""),
            email=user_info["email"],
            address="",  # Google doesn't provide this
            phone_number="",  # Google doesn't provide this
            created_at=user_info.get("iat"),
            updated_at=user_info.get("iat"),
        )
        user = user_repo.create(user_in)

    # Implement session creation, token, etc.
    response = RedirectResponse(url="/")
    # Set cookie/session here
    return response