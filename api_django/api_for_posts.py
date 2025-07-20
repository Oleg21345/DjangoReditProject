from typing import Optional
from fastapi import APIRouter
from fastapi.params import Depends
from fastapi import UploadFile, File
from test_django.models import  Post
from asgiref.sync import sync_to_async
from api_django.schemas.schema_for_post import PostSchema

from api_django.method_for_sql.method import MethodSQL

router = APIRouter(
    tags=["Пости📼"]
)

@router.get("/posts/{title}", summary="Видача конкретного посту")
async def get_one_post(title: str):
    posts = await sync_to_async(Post.objects.get)(title=title)
    return {"posts": posts}


@router.get("/posts", summary="Видача всіх постів")
async def get_all_posts():
    posts = await sync_to_async(list)(Post.objects.values("id", "title", "content", "update_at", "create_at"))
    return {"categories": posts}



@router.post("/posts", summary="Додавання посту")
async def create_post_endpoint(
    post_param: PostSchema = Depends(),
    image: UploadFile | None = File(None)
):
    post_data = post_param.dict()
    post = await MethodSQL.create_post(post_data, image)
    return {"message": "Post created successfully", "post_id": post.id}


@router.put("/posts/{post_id}", summary="Оновлення посту")
async def update_post(
    post_id: int,
    post_param: PostSchema = Depends(),
    image: Optional[UploadFile] = File(None),
):
    post_data = post_param.dict()
    await MethodSQL.update_post_in_db(post_id, post_data, image)
    return {"message": "Пост оновлено успішно"}


@router.delete("/posts/{title}", summary="Видалення посту")
async def delete_category(title: str):
    post = await sync_to_async(Post.objects.get)(title=title)
    await sync_to_async(post.delete)()
    return {"post": "delete success"}


