from fastapi import APIRouter, status
from app.api.deps import MovieManagerDep, GetWatchlistQuery, GetWatchedQuery
from app.schemas.movie import SearchedFilm, GetWatchlistOut, PostWatchlistRequest, PostWatchlistResponse, PostWatchedResponse, PostWatchedRequest, GetWatchedOut
from app.dto.dto import WatchlistFilter, WatchedFilter



router = APIRouter(prefix="/movies", tags=["movie"])



@router.get("/search", response_model=list[SearchedFilm])
async def search_movie(query: str, manager: MovieManagerDep):
    result = await manager.search_movie(query=query)
    return result



@router.get("/watchlist", response_model=list[GetWatchlistOut])
async def get_watchlist(query: GetWatchlistQuery, manager: MovieManagerDep):
    filters = WatchlistFilter(**query.model_dump())
    result = await manager.get_watchlist(filters=filters)
    return result

@router.post("/watchlist", response_model=PostWatchlistResponse)
async def add_to_watchlist(data: PostWatchlistRequest, manager: MovieManagerDep):
    result = await manager.add_to_watchlist(external_id=data.external_id)
    return result

@router.delete("/watchlist/{local_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_from_watchlist(local_id: int, manager: MovieManagerDep):
    await manager.delete_from_watchlist(local_id=local_id)



@router.get("/watched", response_model=list[GetWatchedOut])
async def get_watched(query: GetWatchedQuery, manager: MovieManagerDep):
    filters = WatchedFilter(**query.model_dump())
    result = await manager.get_watched(filters=filters)
    return result

@router.post("/watched", response_model=PostWatchedResponse)
async def add_to_watched(data: PostWatchedRequest, manager: MovieManagerDep):
    result = await manager.add_to_watched(external_id=data.external_id, first_watch=data.first_watch, watched_at=data.watched_at, rating=data.rating, comment=data.comment)
    return result

@router.delete("/watched/{row_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_from_watched(row_id: int, manager: MovieManagerDep):
    await manager.delete_from_watched(row_id=row_id)