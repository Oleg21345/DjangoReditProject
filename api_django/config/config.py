from fastapi import FastAPI
from api_django.config import global_router
from django.conf import settings
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.conf import settings

# FastAPI root path (замінено openapi_prefix → root_path)
mount_path = getattr(settings, "FASTAPI_MOUNT_PATH", "/api")
app = FastAPI(root_path=mount_path)

app.include_router(global_router)
