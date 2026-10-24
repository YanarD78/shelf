from fastapi import APIRouter, status
from app.api.deps import ManagerDep
from app.repositories.diary import MediaType
from app.dto.filters import CompletedFilter, WishlistFilter
from app.api.deps import GetGameSearchQuery, GetWishlistQuery, GetCompletedQuery
from app.schemas.diary import Game, GetCompletedItem, GetCompletedList, GetWishlistItem, GetWishlistList, PatchCompletedRequest, PatchWishlistRequest, PostCompletedRequest, PostCompletedResponse, PostWishlistRequest, PostWishlistResponse, SearchedGame



router = APIRouter(prefix="/games", tags=["game"])



@router.get("/search", response_model=list[SearchedGame])
async def search_game(data: GetGameSearchQuery, manager: ManagerDep):
    return await manager.search_items(type_of=MediaType.game, **data.model_dump(exclude_none=True))

@router.get("/item/{external_id}", response_model=Game)
async def get_game_item(external_id: str, manager: ManagerDep):
    result = await manager.get_item(type_of=MediaType.game, external_id=external_id)
    return Game.from_external(result)



@router.get("/watchlist", response_model=list[GetWishlistList])
async def get_watchlist(query: GetWishlistQuery, manager: ManagerDep):
    filters = WishlistFilter(**query.model_dump())
    return await manager.get_wishlist(type_of=MediaType.game, filters=filters)

@router.get("/watchlist/{row_id}", response_model=GetWishlistItem)
async def get_watchlist_item(row_id: int, manager: ManagerDep):
    return await manager.get_wishlist_item(type_of=MediaType.game, row_id=row_id)

@router.post("/watchlist", response_model=PostWishlistResponse, status_code=status.HTTP_201_CREATED)
async def add_to_watchlist(data: PostWishlistRequest, manager: ManagerDep):
    return await manager.add_to_wishlist(type_of=MediaType.game, external_id=data.external_id, note=data.note)

@router.patch("/watchlist/{row_id}", status_code=status.HTTP_204_NO_CONTENT)
async def edit_watchlist(row_id: int, data: PatchWishlistRequest, manager: ManagerDep):
    await manager.edit_wishlist(row_id=row_id, note=data.note)

@router.delete("/watchlist/{local_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_from_watchlist(local_id: int, manager: ManagerDep):
    await manager.delete_from_wishlist(local_id=local_id)



@router.get("/completed", response_model=list[GetCompletedList])
async def get_completed(query: GetCompletedQuery, manager: ManagerDep):
    filters = CompletedFilter(**query.model_dump())
    return await manager.get_completed(type_of=MediaType.game, filters=filters)

@router.get("/completed/{row_id}", response_model=GetCompletedItem)
async def get_completed_item(row_id: int, manager: ManagerDep):
    return await manager.get_completed_item(type_of=MediaType.game, row_id=row_id)

@router.post("/completed", response_model=PostCompletedResponse, status_code=status.HTTP_201_CREATED)
async def add_to_completed(data: PostCompletedRequest, manager: ManagerDep):
    return await manager.add_to_completed(type_of=MediaType.game, external_id=data.external_id, is_first=data.is_first, completed_on=data.completed_on, rating=data.rating, comment=data.comment)

@router.patch("/completed/{row_id}", status_code=status.HTTP_204_NO_CONTENT)
async def edit_completed(row_id: int, data: PatchCompletedRequest, manager: ManagerDep):
    await manager.edit_completed(row_id=row_id, data=data.model_dump(exclude_unset=True))

@router.delete("/completed/{row_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_from_completed(row_id: int, manager: ManagerDep):
    await manager.delete_from_completed(row_id=row_id)