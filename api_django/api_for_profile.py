from asgiref.sync import sync_to_async
from test_django.models import Profile
from fastapi import APIRouter
from api_django.method_for_sql.method import MethodSQL

router = APIRouter(
    tags=["Профіль🏡"]
)


@router.get("/profiles/{user_id}", summary="Конкретний профіль")
async def get_profile(user_id: int):
    return await MethodSQL.get_profile(user_id)

@router.get("/profiles", summary="Всі профілі")
async def get_profiles():
    profiles = await sync_to_async(list)(Profile.objects.values("user"))
    prof = await MethodSQL.get_subs(profiles)
    return {"profiles": prof}

