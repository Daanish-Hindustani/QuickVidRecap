from fastapi import FastAPI
from app.auth.google_auth import router as google_auth_router
# from app.routes.video import router as video_router
# Import other routers as needed
# from app.routes.user import router as user_router
# from app.routes.subscription import router as subscription_router

app = FastAPI()

# Register all routers
app.include_router(google_auth_router, prefix="/auth", tags=["auth"])
# app.include_router(video_router, prefix="/videos", tags=["videos"])
# app.include_router(user_router, prefix="/users", tags=["users"])
# app.include_router(subscription_router, prefix="/subscriptions", tags=["subscriptions"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)