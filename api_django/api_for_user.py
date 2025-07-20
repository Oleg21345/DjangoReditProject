from asgiref.sync import sync_to_async
from fastapi import APIRouter
from django.contrib.auth.models import User

router = APIRouter(
    tags=["Users🧔👩"]
)

@router.get("/users/{username}", summary="Видача конкретного користувача")
async def get_one_user(username: str):
    users = await sync_to_async(User.objects.get)(username=username)
    user_dict = {
        "id": users.pk,
        "username": users.username,
        "email": users.email,
        "is_active": users.is_active,
    }
    return {"user": user_dict}


@router.get("/users", summary="Видача всіх людей")
async def get_all_user():
    users = await sync_to_async(list)(User.objects.values("id", "username", "email", "is_active"))
    return {"users": users}
