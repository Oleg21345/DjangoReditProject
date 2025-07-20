from fastapi import APIRouter, HTTPException
from test_django.chat_models import GroupMessage, ChatGroup
from api_django.schemas.schema_for_post import GroupMessageSchema, GroupMessageSchemaFile
from asgiref.sync import sync_to_async
from api_django.method_for_sql.method import MethodSQL
from fastapi import UploadFile, File
from fastapi import Form

router = APIRouter(
    tags=["Повідомлення в групі📩"]
)

@router.get("/groupmessages/{chat_group}")
async def chat_group_message(chat_group):
    chatgroup = await sync_to_async(GroupMessage.objects.filter)(chat_group=chat_group)
    chatgroup = await sync_to_async(list)(GroupMessage.objects.values("id", "body", "file", "create_at", "author_id", "chat_group_id"))
    return {"chatgroup": chatgroup}


@router.post("/groupmessages/", response_model=GroupMessageSchema)
async def create_group_message(message_data: GroupMessageSchema):
    return await MethodSQL.post_message(message_data)


@router.post("/groupmessagesfiles/", response_model=GroupMessageSchema)
async def create_group_message(
    chat_group_id: int = Form(...),
    author_id: int = Form(...),
    file: UploadFile = File(...)
):
    return await MethodSQL.post_message_file(chat_group_id, author_id, file)


