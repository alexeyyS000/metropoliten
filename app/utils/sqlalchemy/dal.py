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

    def get_or_create(self, dictions_in_list):
        dictions_in_list.reverse()
        for i in dictions_in_list:
            instance = self.get_one_or_none(**i)
            try:
                instance.scalar_one_or_none()  # почему в случае существования элемента в таюлице методы scalar_one_or_none() и fetchone() кидают ошибки,а в случае None возращают None и ошибки нет
                self.create_one(**i)
            except InvalidRequestError:
                pass
