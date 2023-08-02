from pydantic import BaseModel
import datetime
from typing import Optional
from utils.pydantic import convert_to_optional


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
