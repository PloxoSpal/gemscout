from fastapi import HTTPException
from pydantic import BaseModel
from sqlalchemy import Result, delete, insert, select, update
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession

from backend.database import Base
from backend.repositories.mapper.base import DataMapper

class BaseRepository:
    model: type[Base]
    mapper: type[DataMapper]

    def __init__(self, session) -> None:
        self.session: AsyncSession = session

    async def get_filtered(self, *filters, **filter_by):
        query = select(self.model).filter(*filters).filter_by(**filter_by)
        result: Result = await self.session.execute(query)
        return [
            self.mapper.map_to_domain_entity(data) for data in result.scalars().all()
        ]