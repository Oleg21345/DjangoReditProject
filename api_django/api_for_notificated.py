from asgiref.sync import sync_to_async
from test_django.models import Notificated
from fastapi import APIRouter

router = APIRouter(
    tags=["Сповіщення📬"]
)


@router.get("/notificate/{id}", summary="Сповіщення конкретного користувача")
async def notificated_user(id):
    notificated = await sync_to_async(Notificated.objects.get)(user=id)
    return {"notificated_user": notificated}


