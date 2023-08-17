from db.client import session_maker, test_sesson_marker
from db.dal.post import PostDAL


def get_postdal():
    return PostDAL(session_maker)


def override_get_postdal():
    return PostDAL(test_sesson_marker)
