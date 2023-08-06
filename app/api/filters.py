from db.models import Post
from fastapi_filter.contrib.sqlalchemy import Filter
from typing import Optional, List
import datetime


class PostFilter(Filter):
    name: Optional[str]
    image_url: Optional[str]
    publication_date: Optional[datetime.date]
    order_by: Optional[List[str]]

    class Constants(Filter.Constants):
        model = Post
