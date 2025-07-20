import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()
from fastapi import APIRouter
from test_django.models import Category
from asgiref.sync import sync_to_async


router = APIRouter(
    tags=["Категорії🎲"]
)

@router.get("/categories/{title}", summary="Видача конкретної категорії")
async def get_one_category(title: str):
    categories = await sync_to_async(Category.objects.get)(title=title)
    return {"category": categories}


@router.get("/categories", summary="Видача всіх категорій")
async def get_all_categories():
    categories = await sync_to_async(list)(Category.objects.values("id", "title"))
    return {"categories": categories}


@router.post("/categories", summary="Додавання категорії")
async def post_category(title: str):
    categories = await sync_to_async(Category.objects.create)(title=title)
    return {"categories": "category create success!", "category": categories}

@router.put("/categories/{title}", summary="Оновлення title категорії")
async def put_category(title:str, new_title: str):
    category = await sync_to_async(Category.objects.filter(title=title).update)(title=new_title)
    return {"new_category": True, "category": category}


@router.delete("/categories/{title}", summary="Видалення категорії")
async def delete_category(title: str):
    category = await sync_to_async(Category.objects.get)(title=title)
    await sync_to_async(category.delete)()
    return {"category": "delete success"}










