from fastapi import APIRouter, Depends
from app.api.deps import get_movie_manager
from app.services.movies import MoviesManager
from app.schemas.movies import Film

router = APIRouter()

@router.get("/movies/search", tags=["movie"], response_model=list[Film])
async def search_movie(
    query: str,
    manager: MoviesManager = Depends(get_movie_manager)
):
    result = await manager.search_movie(query)
    return result