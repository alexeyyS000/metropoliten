from fastapi import APIRouter, HTTPException, Depends, status, Query
from api.schemas import PostDetail, PostCreate, PostUpdate, PostPatch, PostPaginatedResponse
from api.filters import PostFilter
from typing import Annotated
from fastapi_filter import FilterDepends
from api.dependencies import get_postdal

router = APIRouter(prefix="/post")


@router.get("/{post_id}", response_model=PostDetail)
def get_one_post(post_id: int, post_dal=Depends(get_postdal)):
    one_post = post_dal.get_one_or_none(id=post_id)
    if one_post is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return one_post


@router.post("/", response_model=PostDetail)
def create_one_post(operation_data: PostCreate, post_dal=Depends(get_postdal)):
    return post_dal.create_one(**operation_data.dict())


@router.put("/{post_id}", response_model=PostDetail)
def update_one_post(post_id: int, operation_data: PostUpdate, post_dal=Depends(get_postdal)):
    updated_post = post_dal.update_one(operation_data.dict(), id=post_id)
    if updated_post is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return updated_post


@router.patch("/{post_id}", response_model=PostDetail)
def patch_one_post(post_id: int, operation_data: PostPatch, post_dal=Depends(get_postdal)):
    patched_post = post_dal.update_one(operation_data.dict(exclude_unset=True), id=post_id)
    if patched_post is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return patched_post


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_one_post(post_id: int, post_dal=Depends(get_postdal)):
    deleted_post = post_dal.delete_one(id=post_id)
    if deleted_post is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return status.HTTP_204_NO_CONTENT


@router.get("/", response_model=PostPaginatedResponse)
def get_pages(
    limit: Annotated[int, Query(ge=1)],
    page: Annotated[int, Query(ge=1)] = 1,
    post_filter: PostFilter = FilterDepends(PostFilter),
    post_dal=Depends(get_postdal),
):
    filter_query = post_filter.filter(post_dal.query())
    query = post_filter.sort(filter_query)
    result, prev_page, next_page, total_pages = post_dal.base(query).fetch(limit, page)
    return PostPaginatedResponse(result=result, prev_page=prev_page, next_page=next_page, total_pages=total_pages)
