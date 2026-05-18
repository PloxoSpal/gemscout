from src.repositories.base import BaseRepository
from src.models.dictionaries import GemTypeOrm
from src.repositories.mapper.dictionaries import GemTypeMapper


class GemTypeRepository(BaseRepository):
    model = GemTypeOrm
    mapper = GemTypeMapper
