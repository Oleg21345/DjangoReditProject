from fastapi import APIRouter
from api_django.api_for_category import router as router_post

global_router = APIRouter(

)

global_router.include_router(router_post)
