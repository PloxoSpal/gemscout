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
        return [self.mapper.to_schema(data) for data in result.scalars().all()]

    async def get_all(self):
        return self.get_filtered()

    async def get_one(self, *filters, **filter_by):
        query = select(self.model).filter(*filters).filter_by(**filter_by)
        result: Result = await self.session.execute(query)
        return self.mapper.to_schema(result.scalars().one_or_none())

    async def add(self, data: BaseModel):
        add_data_stmt = (insert(self.model).values(data.model_dump()).returning())
        result: Result = await self.session.execute(add_data_stmt)
        return self.mapper.to_schema(result.scalars().one())

    async def add_bulk_data(self, data: list[BaseModel]):
        add_bulk_data_stmt = (insert(self.model).values([i.model_dump() for i in data]))
        await self.session.execute(add_bulk_data_stmt)

    async def get_one_or_none(self, **filter_by):
        query = select(self.model).filter_by(**filter_by)
        result: Result = await self.session.execute(query)
        res = result.scalars().one_or_none()
        if res is None:
            return res
        return self.mapper.to_schema(res)

    async def edit(self, data: BaseModel, exclude_unset: bool = False, **filter_by) -> BaseModel:
        try:
            result = await self.get_one_or_none(**filter_by)
        except MultipleResultsFound:
            raise HTTPException(status_code=422, detail="Multiple results")
        if result is None:
            raise HTTPException(status_code=422, detail="Not found")
        edit_data_stmt = (
            update(self.model)
            .filter_by(**filter_by)
            .values(data.model_dump(), exclude_unset=exclude_unset)
            .returning(self.model)
        )
        result: Result = await self.session.execute(edit_data_stmt)
        return self.mapper.to_schema(result.scalars().one())

    async def delete(self, **filter_by) -> None:
        try:
            result = await self.get_one_or_none(**filter_by)
        except MultipleResultsFound:
            raise HTTPException(status_code=422, detail="Multiple results")
        if result is None:
            raise HTTPException(status_code=422, detail="Not found")
        delete_data_stmt = (
            delete(self.model)
            .filter_by(**filter_by)
        )
        await self.session.execute(delete_data_stmt)



