from fastapi import FastAPI
from db.client import session_maker
from db.dal.post import PostDAL

app = FastAPI()

@app.get("/posts/get/get_one_post/{post_id}")
async def get_one_post(post_id: int):
    post_repo = PostDAL(session_maker)
    return post_repo.get_one_or_none(id=post_id)
