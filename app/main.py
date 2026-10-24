import logging
from contextlib import asynccontextmanager
from fastapi.responses import JSONResponse
from fastapi import FastAPI, Request
from httpx import AsyncClient
from app.core.exceptions import AppError
from app.database import engine
from app.api.routers.user import router as user_router
from app.api.routers.movie import router as movie_router
from app.api.routers.game import router as game_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.http = AsyncClient(timeout=10)
    try:
        yield
    finally:
        await app.state.http.aclose()
        await engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.exception_handler(AppError)
async def app_error_handler(request: Request, exc: AppError):
    headers = {"WWW-Authenticate": "Bearer"} if exc.status_code == 401 else None
    return JSONResponse(status_code=exc.status_code, content={"detail": str(exc)}, headers=headers)

@app.exception_handler(Exception)
async def unhandled_error_handler(request: Request, exc: Exception):
    logger.exception("Unhandled error on %s %s", request.method, request.url)
    return JSONResponse(status_code=500, content={"detail": "Internal server error"})

app.include_router(user_router)
app.include_router(movie_router)
app.include_router(game_router)