from src.repositories.mapper.base import DataMapper

from src.models.users import UserOrm
from src.schemas.users import UserResponse

class UserMapper(DataMapper):
    db_model = UserOrm
    schema =UserResponse
