from sqlalchemy import select
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db.models import Post

k = 0
session_maker = sessionmaker(bind=create_engine("postgresql+psycopg://username:password@localhost:5432/database"))
with session_maker() as session:
    stmt = select(Post.id, Post.name, Post.image_url, Post.publication_date, Post.created, Post.updated)
    result = session.execute(stmt)
    for i in result:
        k += 1
        print(k)
        print(i)
        print("__________________________")
