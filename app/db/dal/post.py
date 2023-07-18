from utils.sql.dal import SqlAlchemyRepository
from db.models import Post


class PostDAL(SqlAlchemyRepository):
    class Config:
        model = Post
