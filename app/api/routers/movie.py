from fastapi import APIRouter, status
from app.api.deps import MovieManagerDep
from app.schemas.movies import Film, WatchlistRequest, WatchlistResponse, WatchedRequest, WatchedResponse

router = APIRouter()

@router.get("/movies/search", tags=["movie"], response_model=list[Film])
async def search_movie(query: str, manager: MovieManagerDep):
    result = await manager.search_movie(query=query)
    return result



@router.post("/movies/watchlist", tags=["movie"], response_model=WatchlistResponse)
async def add_to_watchlist(data: WatchlistRequest, manager: MovieManagerDep):
    result = await manager.add_to_watchlist(tmdb_id=data.movie_id)
    return result

@router.delete("/movies/watchlist/{local_movie_id}", tags=["movie"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_from_watchlist(local_movie_id: int, manager: MovieManagerDep):
    await manager.delete_from_watchlist(local_movie_id=local_movie_id)



@router.post("/movies/watched", tags=["movie"], response_model=WatchedResponse)
async def add_to_watched(data: WatchedRequest, manager: MovieManagerDep):
    result = await manager.add_to_watched(tmdb_id=data.movie_id, first_watch=data.first_watch, watched_at=data.watched_at, rating=data.rating, comment=data.comment)
    return result

@router.delete("/movies/watched/{record_id}", tags=["movie"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_from_watched(record_id: int, manager: MovieManagerDep):
    await manager.delete_from_watched(record_id=record_id)