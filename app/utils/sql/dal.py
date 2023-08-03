from sqlalchemy import select
from sqlalchemy import update
from math import ceil


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
            session.commit()  # commit закрывает сессию? так что после нег невозможно обратить ся к instance
            return instance

    def get_or_create(self, default, **kwargs):
        instance = self.get_one_or_none(**kwargs)
        if instance is None:
            return (self.create_one(**(kwargs | default)), True)
        else:
            return (instance, False)

    def update_one(self, attrs: dict, **kwargs):
        with self.session_factory() as session:
            stmt = update(self.Config.model).filter_by(**kwargs).values(**attrs).returning(self.Config.model)
            result = session.execute(stmt)
            session.commit()
            return result.scalar_one_or_none()

    # def update_one1(self, attrs: dict, **kwargs):
    #     instance = self.get_one_or_none(**kwargs)
    #     if instance is None:
    #         return 0
    #     with self.session_factory() as session:
    #         for key, value in attrs.items():
    #             setattr(instance, key, value)
    #         session.add(instance)
    #         session.commit()
    #         return instance

    def delete_one(self, **kwargs):
        instance = self.get_one_or_none(**kwargs)
        if instance is None:
            return None
        with self.session_factory() as session:
            session.delete(instance)
            session.commit()
            return instance

    def fetch(self, limit, page=1, **kwargs):
        if page <= 0 or limit <= 0:
            raise ValueError
        next_page = page + 1
        prev_page = page - 1
        if prev_page == 0:
            prev_page = None
        with self.session_factory() as session:
            stmt = select(self.Config.model).filter_by(**kwargs).offset((page - 1) * limit).limit(limit)
            result = session.execute(stmt).scalars().all()
            total_pages = len(session.execute(select(self.Config.model).filter_by(**kwargs)).scalars().all()) / limit
            return result, {"prev_page": prev_page, "next_page": next_page, "total_pages": ceil(total_pages)}
