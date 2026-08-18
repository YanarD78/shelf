from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from app.core.exceptions import AppError
from app.database import engine, Base
from app.api.routers.user import router as users_router
from app.api.routers.movies import router as movies_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        yield
        await engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.exception_handler(AppError)
async def app_error_handler(request, exc: AppError):
    return JSONResponse(status_code=exc.status_code, content={"detail": str(exc)})

app.include_router(users_router)
app.include_router(movies_router)