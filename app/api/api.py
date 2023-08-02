from fastapi import APIRouter, HTTPException, Depends
from db.client import session_maker
from db.dal.post import PostDAL
from .schemas import PostDetail, PostCreate, PostUpdate, PostPatch, SortModel
from typing import List

router = APIRouter(prefix="/post")


@router.get("/get_one/{post_id}", response_model=PostDetail)
def get_one_post(post_id: int):
    one_post = PostDAL(session_maker).get_one_or_none(id=post_id)
    if one_post is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return one_post


@router.post("/create_one/", response_model=PostDetail)
def create_one_post(operation_data: PostCreate):
    return PostDAL(session_maker).create_one(**operation_data.dict())


@router.put("/put_one/{post_id}", response_model=PostDetail)
def update_one_post(post_id: int, operation_data: PostUpdate):
    updated_post = PostDAL(session_maker).update_one(operation_data.dict(), id=post_id)
    if updated_post is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_post


@router.patch("/patch_one/{post_id}", response_model=PostDetail)
def patch_one_post(post_id: int, operation_data: PostPatch):
    patched_post = PostDAL(session_maker).update_one(operation_data.dict(exclude_unset=True), id=post_id)
    if patched_post is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return patched_post


@router.delete("/delete_one/", response_model=PostDetail)
def delete_one_post(post_id: int):
    deleted_post = PostDAL(session_maker).delete_one(id=post_id)
    if deleted_post is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return deleted_post


@router.get("/get_some_amount/", response_model=List[PostDetail])
def get_some_amount(limit: int, page: int, criteria: SortModel = Depends()):
    criteria_dict = criteria.dict()
    dictrem = {keys: values for keys, values in criteria_dict.items() if values is not None}
    print(dictrem)
    return PostDAL(session_maker).fetch2(limit, page, **dictrem)
