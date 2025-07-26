import os
from fastapi import FastAPI, Request, Depends
from fastapi.responses import HTMLResponse
from starlette.middleware.sessions import SessionMiddleware

from app.auth.google_auth import router as google_auth_router, get_current_user

app = FastAPI()

# === Middleware ===
SESSION_SECRET = os.environ.get("SESSION_SECRET_KEY", "dev-session-fallback")
app.add_middleware(SessionMiddleware, secret_key=SESSION_SECRET)

# === Routers ===
app.include_router(google_auth_router, prefix="/auth", tags=["auth"])

# === Routes ===
@app.get("/", response_class=HTMLResponse)
async def root(request: Request, user=Depends(get_current_user)) -> str:
    email = user.get("email", "Unknown")
    return f"""
        <h1>✅ Login Successful</h1>
        <p>Welcome, {email}!</p>
        <p><a href="/auth/logout">Logout</a></p>
    """

@app.get("/public", response_class=HTMLResponse)
async def public_home() -> str:
    return """
        <h1>🔓 Public Page</h1>
        <p><a href="/auth/login/google">Login with Google</a></p>
    """
