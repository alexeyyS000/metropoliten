from pydantic import BaseModel
import datetime
from typing import Optional
from utils.pydantic import convert_to_optional
from db.models import Post as ORMPost
from fastapi_filter.contrib.sqlalchemy import Filter
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


# @dataclass
class SortModel(BaseModel):
    name: Optional[str]
    publication_date: Optional[datetime.date]


class PostFilter(Filter):
    name: Optional[str]
    publication_date: Optional[datetime.date]
    order_by: List[str] = ["publication_date"]

    class Constants(Filter.Constants):
        model = ORMPost


class ResponsPostFilter(BaseModel):
    result: List[PostDetail]
    prev_page: Optional[int]
    next_page: Optional[int]
    total_pages: int
