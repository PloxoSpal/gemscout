from src.models.users import UserOrm
from src.repositories.base import BaseRepository

from src.repositories.mapper.users import UserMapper

class UserRepository(BaseRepository):
    model = UserOrm
    mapper = UserMapper

    