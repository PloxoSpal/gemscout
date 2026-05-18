from src.repositories.mapper.base import DataMapper
from src.models.dictionaries import GemTypeOrm
from src.schemas.dictionaries import GemTypeResponse

class GemTypeMapper(DataMapper):
    db_model = GemTypeOrm
    schema = GemTypeResponse