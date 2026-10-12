from fastapi import APIRouter, status
from app.api.deps import ManagerDep, GetWishlistQuery, GetCompletedQuery, GetSearchQuery
from app.schemas.movie import SearchedMovie, Movie, GetWishlistOut, GetCompletedOut, PostCompletedRequest, PatchWishlistRequest, PatchCompletedRequest, PostCompletedResponse, PostWishlistRequest, PostWishlistResponse
from app.dto.filters import WishlistFilter, CompletedFilter
from app.models.media import MediaType



router = APIRouter(prefix="/movies", tags=["movie"])



@router.get("/search", response_model=list[SearchedMovie])
async def search_movie(data: GetSearchQuery, manager: ManagerDep):
    return await manager.search_items(type_of=MediaType.movie, query=data.query, page=data.page)

@router.get("/item/{external_id}", response_model=Movie)
async def get_movie_item(external_id: str, manager: ManagerDep):
    result = await manager.get_item(type_of=MediaType.movie, external_id=external_id)
    return Movie.from_external(result)



@router.get("/watchlist", response_model=list[GetWishlistOut])
async def get_watchlist(query: GetWishlistQuery, manager: ManagerDep):
    filters = WishlistFilter(**query.model_dump())
    return await manager.get_wishlist(type_of=MediaType.movie, filters=filters)

@router.post("/watchlist", response_model=PostWishlistResponse, status_code=status.HTTP_201_CREATED)
async def add_to_watchlist(data: PostWishlistRequest, manager: ManagerDep):
    return await manager.add_to_wishlist(type_of=MediaType.movie, external_id=data.external_id, note=data.note)

@router.patch("/watchlist/{local_id}", status_code=status.HTTP_204_NO_CONTENT)
async def edit_watchlist(local_id: int, data: PatchWishlistRequest, manager: ManagerDep):
    await manager.edit_wishlist(local_id=local_id, note=data.note)

@router.delete("/watchlist/{local_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_from_watchlist(local_id: int, manager: ManagerDep):
    await manager.delete_from_wishlist(local_id=local_id)



@router.get("/watched", response_model=list[GetCompletedOut])
async def get_watched(query: GetCompletedQuery, manager: ManagerDep):
    filters = CompletedFilter(**query.model_dump())
    return await manager.get_completed(type_of=MediaType.movie, filters=filters)

@router.post("/watched", response_model=PostCompletedResponse, status_code=status.HTTP_201_CREATED)
async def add_to_watched(data: PostCompletedRequest, manager: ManagerDep):
    return await manager.add_to_completed(type_of=MediaType.movie, external_id=data.external_id, is_first=data.is_first, completed_on=data.completed_on, rating=data.rating, comment=data.comment)

@router.patch("/watched/{row_id}", status_code=status.HTTP_204_NO_CONTENT)
async def edit_watched(row_id: int, data: PatchCompletedRequest, manager: ManagerDep):
    await manager.edit_watched(row_id=row_id, data=data.model_dump(exclude_unset=True))

@router.delete("/watched/{row_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_from_watched(row_id: int, manager: ManagerDep):
    await manager.delete_from_completed(row_id=row_id)