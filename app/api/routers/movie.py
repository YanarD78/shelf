from fastapi import APIRouter
from app.api.deps import MovieManagerDep
from app.schemas.movies import Film

router = APIRouter()

@router.get("/movies/search", tags=["movie"], response_model=list[Film])
async def search_movie(query: str, manager: MovieManagerDep):
    result = await manager.search_movie(query)
    return result