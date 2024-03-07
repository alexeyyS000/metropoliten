from db.client import session_maker
from db.dal.post import PostDAL


def get_postdal():
    return PostDAL(session_maker)
