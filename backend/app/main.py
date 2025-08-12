# backend/app/main.py
import os
import sys
from fastapi import FastAPI
from loguru import logger
from .core import config, logging as log_config
from .api.v1 import posts, users
import sentry_sdk
from sentry_sdk.integrations.starlette import StarletteIntegration

# Initialize Sentry for error monitoring
SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    sentry_sdk.init(dsn=SENTRY_DSN, integrations=[StarletteIntegration()])

app = FastAPI(
    title="MyProject API",
    description="Backend API for MyProject",
    version="1.0.0",
    docs_url="/docs", redoc_url="/redoc"  # Swagger UI and ReDoc
)

# Set up logging (Loguru)
logger.remove()  # remove default logger
# Add a rotating file logger and console logger
logger.add("logs/app.log", rotation="1 week", retention="4 weeks",
           backtrace=True, diagnose=True, level="INFO")
logger.add(sys.stderr, level="INFO")  # also log to stderr for Docker

# Include API routers  
app.include_router(users.router, prefix="/api/v1", tags=["users"])
app.include_router(posts.router, prefix="/api/v1", tags=["posts"])

@app.get("/")
async def root():
    return {"message": "API is running"}
