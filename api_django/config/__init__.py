from fastapi import APIRouter
from api_django.api_for_category import router as router_category
from api_django.api_for_posts import router as router_posts
from api_django.api_for_profile import router as router_profile
from api_django.api_for_user import router as router_user
from api_django.api_for_notificated import router as router_notificated
from api_django.api_for_chats import router as router_chat

global_router = APIRouter(

)

global_router.include_router(router_category)
global_router.include_router(router_posts)
global_router.include_router(router_profile)
global_router.include_router(router_user)
global_router.include_router(router_notificated)
global_router.include_router(router_chat)