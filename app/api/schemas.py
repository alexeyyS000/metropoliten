from pydantic import BaseModel
import datetime
from typing import Optional
from utils.pydantic import convert_to_optional
from typing import List


class Post(BaseModel):
    name: str
    image_url: Optional[str]
    publication_date: datetime.date


class PostDetail(Post):
    id: int
    created: datetime.datetime
    updated: Optional[datetime.datetime]

    class Config:
        orm_mode = True


class PostCreate(Post):
    pass


class PostUpdate(Post):
    pass


class PostDelete(Post):
    pass


class PostPatch(Post):
    __annotations__ = convert_to_optional(Post)


class PostPaginatedResponse(BaseModel):
    result: List[PostDetail]
    prev_page: Optional[int]
    next_page: Optional[int]
    total_pages: int
