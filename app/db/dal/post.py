from utils.sqlalchemy import SqlAlchemyRepository
from db.models import Post


class PostDAL(SqlAlchemyRepository):
    class Config:
        model = Post
