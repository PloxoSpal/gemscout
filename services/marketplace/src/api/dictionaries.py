from fastapi import APIRouter

from src.api.dependencies.db import DBDep
from src.schemas.dictionaries import GemTypeRequest

router = APIRouter(prefix="/dictionaries", tags=["Dictionaries"])

@router.get("/types")
async def get_gem_types(db: DBDep):
    gem_types = await db.gem_types.get_all()
    return {"status": "success", "data": gem_types}

@router.post("/types")
async def post_gem_types(data: GemTypeRequest, db: DBDep):
    new_gem_types = await db.gem_types.add(data)
    await db.commit()
    return {"status": "success", "data": new_gem_types}