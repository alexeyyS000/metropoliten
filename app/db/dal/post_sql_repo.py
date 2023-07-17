from utils.sqlalchemy import SqlAlchemyRepository
from db.models import Post


class PostDAl(SqlAlchemyRepository):
    class Config:
        model = Post
