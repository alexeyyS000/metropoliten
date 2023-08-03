from fastapi import APIRouter, HTTPException, Depends, status, Query
from db.client import session_maker
from db.dal.post import PostDAL
from .schemas import PostDetail, PostCreate, PostUpdate, PostPatch, SortModel
from typing import Annotated

router = APIRouter(prefix="/post")


@router.get("/{post_id}", response_model=PostDetail)
def get_one_post(post_id: int):
    one_post = PostDAL(session_maker).get_one_or_none(id=post_id)
    if one_post is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return one_post


@router.post("/", response_model=PostDetail)
def create_one_post(operation_data: PostCreate):
    return PostDAL(session_maker).create_one(**operation_data.dict())


@router.put("/", response_model=PostDetail)
def update_one_post(post_id: int, operation_data: PostUpdate):
    updated_post = PostDAL(session_maker).update_one(operation_data.dict(), id=post_id)
    if updated_post is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_post


@router.patch("/", response_model=PostDetail)
def patch_one_post(post_id: int, operation_data: PostPatch):
    patched_post = PostDAL(session_maker).update_one(operation_data.dict(exclude_unset=True), id=post_id)
    if patched_post is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return patched_post


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_one_post(post_id: int):
    deleted_post = PostDAL(session_maker).delete_one(id=post_id)
    if deleted_post is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return status.HTTP_204_NO_CONTENT


@router.get("/")
def get_some_amount(
    limit: Annotated[int, Query(ge=1)], page: Annotated[int, Query(ge=1)], criteria: SortModel = Depends()
):
    criteria_dict = criteria.dict()
    dictrem = {keys: values for keys, values in criteria_dict.items() if values is not None}
    print(dictrem)
    return PostDAL(session_maker).fetch(limit, page, **dictrem)
