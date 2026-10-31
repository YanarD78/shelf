from fastapi import APIRouter, status
from app.api.deps import DiaryServiceDep
from app.repositories.diary import MediaType
from app.dto.filters import CompletedFilter, WishlistFilter
from app.api.deps import GetGameSearchQuery, GetWishlistQuery, GetCompletedQuery
from app.schemas.diary import Game, GetCompletedItem, GetCompletedList, GetWishlistItem, GetWishlistList, PatchCompletedRequest, PatchWishlistRequest, PostCompletedRequest, PostCompletedResponse, PostWishlistRequest, PostWishlistResponse, SearchedGame



router = APIRouter(prefix="/games", tags=["game"])



@router.get("/search", response_model=list[SearchedGame])
async def search_game(data: GetGameSearchQuery, service: DiaryServiceDep):
    return await service.search_items(type_of=MediaType.game, **data.model_dump(exclude_none=True))

@router.get("/item/{external_id}", response_model=Game)
async def get_game_item(external_id: str, service: DiaryServiceDep):
    result = await service.get_item(type_of=MediaType.game, external_id=external_id)
    return Game.from_external(result)



@router.get("/wishlist", response_model=list[GetWishlistList])
async def get_wishlist(query: GetWishlistQuery, service: DiaryServiceDep):
    filters = WishlistFilter(**query.model_dump())
    return await service.get_wishlist(type_of=MediaType.game, filters=filters)

@router.get("/wishlist/{row_id}", response_model=GetWishlistItem)
async def get_wishlist_item(row_id: int, service: DiaryServiceDep):
    return await service.get_wishlist_item(type_of=MediaType.game, row_id=row_id)

@router.post("/wishlist", response_model=PostWishlistResponse, status_code=status.HTTP_201_CREATED)
async def add_to_wishlist(data: PostWishlistRequest, service: DiaryServiceDep):
    return await service.add_to_wishlist(type_of=MediaType.game, external_id=data.external_id, note=data.note)

@router.patch("/wishlist/{row_id}", status_code=status.HTTP_204_NO_CONTENT)
async def edit_wishlist(row_id: int, data: PatchWishlistRequest, service: DiaryServiceDep):
    await service.edit_wishlist(row_id=row_id, note=data.note)

@router.delete("/wishlist/{local_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_from_wishlist(local_id: int, service: DiaryServiceDep):
    await service.delete_from_wishlist(local_id=local_id)



@router.get("/completed", response_model=list[GetCompletedList])
async def get_completed(query: GetCompletedQuery, service: DiaryServiceDep):
    filters = CompletedFilter(**query.model_dump())
    return await service.get_completed(type_of=MediaType.game, filters=filters)

@router.get("/completed/{row_id}", response_model=GetCompletedItem)
async def get_completed_item(row_id: int, service: DiaryServiceDep):
    return await service.get_completed_item(type_of=MediaType.game, row_id=row_id)

@router.post("/completed", response_model=PostCompletedResponse, status_code=status.HTTP_201_CREATED)
async def add_to_completed(data: PostCompletedRequest, service: DiaryServiceDep):
    return await service.add_to_completed(type_of=MediaType.game, external_id=data.external_id, is_first=data.is_first, completed_on=data.completed_on, rating=data.rating, comment=data.comment)

@router.patch("/completed/{row_id}", status_code=status.HTTP_204_NO_CONTENT)
async def edit_completed(row_id: int, data: PatchCompletedRequest, service: DiaryServiceDep):
    await service.edit_completed(row_id=row_id, data=data.model_dump(exclude_unset=True))

@router.delete("/completed/{row_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_from_completed(row_id: int, service: DiaryServiceDep):
    await service.delete_from_completed(row_id=row_id)