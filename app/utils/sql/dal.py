from sqlalchemy import select


class SqlAlchemyRepository:
    class Config:
        model = None

    def __init__(self, session_factory):
        self.session_factory = session_factory

    def get_one_or_none(self, **kwargs):
        with self.session_factory() as session:
            stmt = select(self.Config.model).filter_by(**kwargs)
            result = session.execute(stmt)
            return result.scalar_one_or_none()

    def create_one(self, **kwargs):
        with self.session_factory() as session:
            instance = self.Config.model(**kwargs)
            session.add(instance)
            session.commit()
            return instance

    def get_or_create(self, default, **kwargs):
        instance = self.get_one_or_none(**kwargs)
        if instance is None:
            return (self.create_one(**(kwargs | default)), True)
        else:
            return (instance, False)
