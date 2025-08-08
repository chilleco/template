# backend/app/main.py
import os
from fastapi import FastAPI, WebSocket
from loguru import logger
from .core import config, logging as log_config
from .api import posts, users, chat
import sentry_sdk
from sentry_sdk.integrations.fastapi import FastAPIIntegration

# Initialize Sentry for error monitoring
SENTRY_DSN = os.getenv("SENTRY_DSN")
if SENTRY_DSN:
    sentry_sdk.init(dsn=SENTRY_DSN, integrations=[FastAPIIntegration()])

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
app.include_router(users.router, prefix="/api/users", tags=["users"])
app.include_router(posts.router, prefix="/api/posts", tags=["posts"])
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

# Example WebSocket endpoint for live chat (within chat router or here)
@app.websocket("/ws/chat")
async def chat_websocket(ws: WebSocket):
    await ws.accept()
    user = await authenticate_ws(ws)  # pseudocode: authenticate the user for WS
    CONNECTIONS.add(user.id, ws)      # add to some global connection manager
    try:
        while True:
            data = await ws.receive_text()
            # Broadcast the message to other users (via Redis pub/sub or in-memory)
            await broadcast_message(user, data)
    except WebSocketDisconnect:
        CONNECTIONS.remove(user.id)
