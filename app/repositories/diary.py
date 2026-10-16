from app.core.exceptions import RecordAlreadyExists
from app.dto.filters import WishlistFilter, CompletedFilter
from app.models.diary import Wishlist, Completed
from app.models.media import ContentItem, Movie
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import insert, delete, select, update, func
from sqlalchemy.dialects.postgresql import insert as pg_insert
from sqlalchemy.orm import contains_eager, load_only
from datetime import date
from typing import Sequence
from app.models.media import MediaType, ExternalType
from app.dto.external import ExternalItem

MODEL_BY_TYPE: dict[MediaType, type[ContentItem]] = {
    MediaType.movie: Movie
}

SOURCE_BY_TYPE: dict[MediaType, ExternalType] = {
    MediaType.movie: ExternalType.tmdb
}



class DiaryRepo:
    """A class designed to interact with the database for searching and adding movies, games, and books"""
    def __init__(self, session: AsyncSession):
        self.session = session



    async def get_item(self, type_of: MediaType, external_id: str) -> int | None:
        stmt = (select(ContentItem.id)
            .where(ContentItem.media_type==type_of)
            .where(ContentItem.external_id==external_id)
            .where(ContentItem.source==SOURCE_BY_TYPE[type_of]))
        result = await self.session.execute(stmt)
        return result.scalar()

    

    async def add_item(self, type_of: MediaType, item: ExternalItem) -> int:
        model = MODEL_BY_TYPE[type_of]
        obj = model(
            media_type=type_of,
            title=item.title,
            description=item.description,
            cover_url=item.cover_url,
            vote_average=item.vote_average,
            release_date=item.release_date,
            external_id=item.external_id,
            source=SOURCE_BY_TYPE[type_of],
            **item.extra
        )

        try:
            async with self.session.begin_nested():
                self.session.add(obj)
                await self.session.flush()
                return obj.id
        except IntegrityError:
            return await self.get_item(type_of=type_of, external_id=item.external_id)



    async def get_wishlist(self, type_of: MediaType, user_id: int, filters: WishlistFilter) -> Sequence[Wishlist]:
        stmt = (select(Wishlist)
            .join(Wishlist.content)
            .options(
                load_only(
                    Wishlist.id,
                    Wishlist.local_id,
                    Wishlist.note,
                    Wishlist.created_at
                ),
                contains_eager(Wishlist.content).load_only(
                    ContentItem.external_id,
                    ContentItem.title,
                    ContentItem.description,
                    ContentItem.release_date,
                    ContentItem.cover_url,
                    ContentItem.vote_average
                )
            )
            .where(Wishlist.user_id == user_id)
            .where(ContentItem.media_type==type_of))

        if filters.added_before is not None:
            stmt = stmt.where(func.date(Wishlist.created_at) < filters.added_before)
        if filters.added_after is not None:
            stmt = stmt.where(func.date(Wishlist.created_at) > filters.added_after)
        if filters.added_at is not None:
            stmt = stmt.where(func.date(Wishlist.created_at) == filters.added_at)

        if filters.released_before is not None:
            stmt = stmt.where(ContentItem.release_date < filters.released_before)
        if filters.released_after is not None:
            stmt = stmt.where(ContentItem.release_date > filters.released_after)
        if filters.released_at is not None:
            stmt = stmt.where(ContentItem.release_date == filters.released_at)

        if filters.limit is not None:
            stmt = stmt.limit(limit=filters.limit)
        if filters.offset is not None:
            stmt = stmt.offset(offset=filters.offset)

        stmt = stmt.order_by(Wishlist.created_at.desc()).order_by(Wishlist.id.desc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def get_wishlist_item(self, type_of: MediaType, user_id: int, row_id: int) -> Wishlist | None:
        stmt = (select(Wishlist)
            .join(Wishlist.content)
            .options(contains_eager(Wishlist.content))
            .where(Wishlist.user_id == user_id, Wishlist.id == row_id)
            .where(ContentItem.media_type == type_of))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add_to_wishlist(self, user_id: int, local_id: int, note: str | None) -> int:
        stmt = (pg_insert(Wishlist)
            .values(user_id=user_id, local_id=local_id, note=note)
            .on_conflict_do_nothing(constraint="uq_wishlist_user")
            .returning(Wishlist.id))
        result = (await self.session.execute(stmt)).scalar_one_or_none()
        if result is None:
            raise RecordAlreadyExists()
        return result

    async def edit_wishlist(self, user_id: int, row_id: int, note: str | None) -> int | None:
        stmt = (update(Wishlist)
            .where(Wishlist.user_id==user_id, Wishlist.id==row_id)
            .values(note=note)
            .returning(Wishlist.id))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_from_wishlist(self, user_id: int, local_id: int) -> int | None:
        stmt = delete(Wishlist).where(
            Wishlist.user_id==user_id,
            Wishlist.local_id==local_id
        ).returning(Wishlist.id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()



    async def get_completed(self, type_of: str, user_id: int, filters: CompletedFilter) -> Sequence:
        stmt = (select(Completed)
            .join(Completed.content)
            .options(
                load_only(
                    Completed.id,
                    Completed.local_id,
                    Completed.is_first,
                    Completed.rating,
                    Completed.completed_on,
                    Completed.comment,
                    Completed.created_at
                ),
                contains_eager(Completed.content).load_only(
                    ContentItem.external_id,
                    ContentItem.title,
                    ContentItem.description,
                    ContentItem.release_date,
                    ContentItem.cover_url,
                    ContentItem.vote_average
                ))
            .where(Completed.user_id == user_id)
            .where(ContentItem.media_type == type_of))
        
        if filters.local_id is not None:
            stmt = stmt.where(Completed.local_id == filters.local_id)

        if filters.completed_before is not None:
            stmt = stmt.where(Completed.completed_on < filters.completed_before)
        if filters.completed_after is not None:
            stmt = stmt.where(Completed.completed_on > filters.completed_after)
        if filters.completed_at is not None:
            stmt = stmt.where(Completed.completed_on == filters.completed_at)

        if filters.limit is not None:
            stmt = stmt.limit(limit=filters.limit)
        if filters.offset is not None:
            stmt = stmt.offset(offset=filters.offset)

        stmt = stmt.order_by(Completed.completed_on.desc().nulls_last()).order_by(Completed.id.desc())
        result = await self.session.execute(stmt)
        return result.unique().scalars().all()

    async def get_completed_item(self, type_of: MediaType, user_id: int, row_id: int) -> Completed | None:
        stmt = (select(Completed)
            .join(Completed.content)
            .options(contains_eager(Completed.content))
            .where(Completed.user_id == user_id, Completed.id == row_id)
            .where(ContentItem.media_type == type_of))
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def add_to_completed(self, user_id: int, local_id: int, is_first: bool, completed_on: date | None, rating: float | None, comment: str | None) -> int:
        if is_first:
            update_stmt = update(Completed).where(
                Completed.user_id==user_id,
                Completed.local_id==local_id,
                Completed.is_first==is_first
            ).values(is_first=False)
            await self.session.execute(update_stmt)

        stmt = insert(Completed).values(
            user_id=user_id,
            local_id=local_id,
            is_first=is_first,
            completed_on=completed_on,
            rating=rating,
            comment=comment
        ).returning(Completed.id)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def edit_completed(self, user_id: int, row_id: int, data: dict) -> int | None:
        stmt = update(Completed).where(
            Completed.user_id==user_id,
            Completed.id==row_id
        ).values(**data).returning(Completed.id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def delete_from_completed(self, user_id: int, row_id: int) -> int | None:
        stmt = delete(Completed).where(
            Completed.user_id==user_id,
            Completed.id==row_id
        ).returning(Completed.id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()