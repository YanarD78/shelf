from fastapi import APIRouter, status
from app.api.deps import MovieManagerDep
from app.schemas.movies import Film, WatchlistRequest, WatchlistResponse

router = APIRouter()

@router.get("/movies/search", tags=["movie"], response_model=list[Film])
async def search_movie(query: str, manager: MovieManagerDep):
    result = await manager.search_movie(query=query)
    return result

@router.post("/movies/watchlist", tags=["movie"], response_model=WatchlistResponse)
async def add_to_watchlist(data: WatchlistRequest, manager: MovieManagerDep):
    result = await manager.add_to_watchlist(movie_id=data.movie_id)
    return result

@router.delete("/movies/watchlist/{movie_id}", tags=["movie"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_from_watchlist(movie_id: int, manager: MovieManagerDep):
    await manager.delete_from_watchlist(movie_id=movie_id)