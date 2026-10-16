from app.repositories.diary import DiaryRepo
from app.repositories.user import UserRepo
from app.core.exceptions import ItemNotFound
from app.dto.filters import WishlistFilter, CompletedFilter
from app.dto.external import ExternalItem
from app.providers.base import MediaProvider
from app.models.media import MediaType
from typing import Sequence
from datetime import date

class Manager:
    """A class designed for searching for movies, books, games and saving them"""
    def __init__(self, providers: dict[MediaType, MediaProvider], users_repo: UserRepo, diary_repo: DiaryRepo, current_user: int):
        self.providers = providers
        self.users_repo = users_repo
        self.diary_repo = diary_repo
        self.user = current_user



    async def _resolve_local_id(self, type_of: MediaType, external_id: str) -> int:
        local_id = await self.diary_repo.get_item(type_of=type_of, external_id=external_id)
        if local_id is None:
            item = await self.providers[type_of].get(external_id=external_id)
            local_id = await self.diary_repo.add_item(type_of=type_of, item=item)
        return local_id



    async def search_items(self, type_of: MediaType, query: str, page: int) -> list[ExternalItem]:
        preferences = await self.users_repo.get_user_preferences(user_id=self.user)

        return await self.providers[type_of].search(
            query=query,
            include_adult=preferences.include_adult,
            page=page
        )

    async def get_item(self, type_of: MediaType, external_id: str) -> ExternalItem:
        return await self.providers[type_of].get(external_id=external_id)



    async def get_wishlist(self, type_of: MediaType, filters: WishlistFilter) -> Sequence:
        return await self.diary_repo.get_wishlist(type_of=type_of, user_id=self.user, filters=filters)

    async def get_wishlist_item(self, type_of: MediaType, row_id: int):
        result = await self.diary_repo.get_wishlist_item(type_of=type_of, user_id=self.user, row_id=row_id)
        if result is None:
            raise ItemNotFound
        return result

    async def add_to_wishlist(self, type_of: MediaType, external_id: str, note: str | None) -> dict[str, int]:
        local_id = await self._resolve_local_id(type_of=type_of, external_id=external_id)
        result = await self.diary_repo.add_to_wishlist(
            user_id=self.user,
            local_id=local_id,
            note=note
        )
        return {"id": result, "local_id": local_id}

    async def edit_wishlist(self, row_id: int, note: str | None) -> None:
        result = await self.diary_repo.edit_wishlist(user_id=self.user, row_id=row_id, note=note)
        if result is None:
            raise ItemNotFound()

    async def delete_from_wishlist(self, local_id: int) -> None:
        result = await self.diary_repo.delete_from_wishlist(user_id=self.user, local_id=local_id)
        if result is None:
            raise ItemNotFound()



    async def get_completed(self, type_of: MediaType, filters: CompletedFilter) -> Sequence:
        return await self.diary_repo.get_completed(type_of=type_of, user_id=self.user, filters=filters)

    async def get_completed_item(self, type_of: MediaType, row_id: int):
        result = await self.diary_repo.get_completed_item(type_of=type_of, user_id=self.user, row_id=row_id)
        if result is None:
            raise ItemNotFound
        return result

    async def add_to_completed(self, type_of: MediaType, external_id: str, is_first: bool, completed_on: date | None, rating: float | None, comment: str | None) -> dict[str, int]:
        local_id = await self._resolve_local_id(type_of=type_of, external_id=external_id)
        result = await self.diary_repo.add_to_completed(
            user_id=self.user,
            local_id=local_id,
            is_first=is_first,
            completed_on=completed_on,
            rating=rating,
            comment=comment,
        )
        return {"id": result, "local_id": local_id}

    async def edit_watched(self, row_id: int, data: dict) -> None:
        result = await self.diary_repo.edit_completed(
            user_id=self.user,
            row_id=row_id,
            data=data
        )
        if result is None:
            raise ItemNotFound()

    async def delete_from_completed(self, row_id: int) -> None:
        result = await self.diary_repo.delete_from_completed(
            user_id=self.user,
            row_id=row_id
        )
        if result is None:
            raise ItemNotFound()