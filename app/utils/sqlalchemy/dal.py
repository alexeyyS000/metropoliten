from sqlalchemy import select
from sqlalchemy.exc import InvalidRequestError


class SqlAlchemyRepository:
    class Config:
        model = None

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def get_one_or_none(self, **kwargs):
        with self.session_factory() as session:
            stmt = select(self.Config.model).filter_by(**kwargs)
            result = session.execute(stmt)
            return result

    def create_one(self, **kwargs):
        with self.session_factory() as session:
            session.add(self.Config.model(**kwargs))
            session.commit()

    def get_or_create(self, **kwargs):
        instance=self.get_one_or_none(**kwargs)
        try:
            instance.scalar_one_or_none()
            self.create_one(**kwargs)
        except InvalidRequestError:
            return instance