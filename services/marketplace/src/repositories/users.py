from services.marketplace.src.models.users import UserOrm
from services.marketplace.src.repositories.base import BaseRepository


class UsersRepository(BaseRepository):
    model = UserOrm
    mapper = models.User