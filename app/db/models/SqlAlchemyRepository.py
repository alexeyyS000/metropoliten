from sqlalchemy import select
from db.models.post import Post


class SqlAlchemyRepository:
    def __init__(self, session_factory):
        self.session_factory = session_factory

    def get_one_or_none(self, diction):
        with self.session_factory() as session:
            stmt = select(Post.name).where(Post.id == diction["tag"])
            result = session.execute(stmt)
            return result

    def create_one(self, diction):
        with self.session_factory() as session:
            session.add(Post(id=diction["tag"], name=diction["headline"], image_url=diction["url"]))
            session.commit()


class Get_or_create(SqlAlchemyRepository):
    def get_or_create(self, dictions_in_list):
        for i in dictions_in_list:
            instance = self.get_one_or_none(i)
            try:
                next(iter(instance))
            except StopIteration:
                self.create_one(i)
