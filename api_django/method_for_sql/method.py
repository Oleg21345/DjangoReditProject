from test_django.models import Category, Post
from fastapi import UploadFile
from config import settings
import shutil
import os
import uuid
from typing import Optional
from test_django.models import Profile
from fastapi import HTTPException
from test_django.chat_models import GroupMessage, ChatGroup
from asgiref.sync import sync_to_async
from django.contrib.auth.models import User
from django.core.files.uploadedfile import SimpleUploadedFile


class MethodSQL:
    @staticmethod
    async def update_post_in_db(post_id: int, post_data: dict, image: Optional[UploadFile] = None):
        post = await sync_to_async(Post.objects.get)(id=post_id)

        category = await sync_to_async(Category.objects.get)(id=post_data.pop("category_id"))
        author = await sync_to_async(User.objects.get)(id=post_data.pop("author_id"))

        post.category = category
        post.author = author

        for field, value in post_data.items():
            setattr(post, field, value)

        if image:
            upload_path = os.path.join(settings.MEDIA_ROOT, "photos", image.filename)
            with open(upload_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            post.image = f"photos/{image.filename}"

        await sync_to_async(post.save)()

    @staticmethod
    async def create_post(post_data: dict, image: UploadFile | None = None):
        category_id = post_data.pop("category_id")
        author_id = post_data.pop("author_id")

        try:
            category = await sync_to_async(Category.objects.get)(id=category_id)
        except Category.DoesNotExist:
            raise HTTPException(status_code=404, detail="Category not found")

        try:
            author = await sync_to_async(User.objects.get)(id=author_id)
        except User.DoesNotExist:
            raise HTTPException(status_code=404, detail="Author not found")

        if image:
            filename = f"{uuid.uuid4()}_{image.filename}"
            save_dir = os.path.join("media", "photos")
            os.makedirs(save_dir, exist_ok=True)
            save_path = os.path.join(save_dir, filename)
            with open(save_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            post_data["image"] = f"photos/{filename}"

        post = await sync_to_async(Post.objects.create)(
            category_id=category,
            author=author,
            **post_data
        )
        return post

    @staticmethod
    async def get_profile(user_id: int):
        try:
            profile = await sync_to_async(Profile.objects.get)(user__id=user_id)
        except Profile.DoesNotExist:
            raise HTTPException(status_code=404, detail="Profile not found")

        def extract_profile_data(p):
            return {
                "user_id": p.user.id,
                "subscribers_ids": list(p.subscribers.values_list("id", flat=True)),
                "subscriptions_ids": list(p.subscriptions.values_list("id", flat=True)),
                "avatars": p.avatars.url if p.avatars else None,
            }

        profile_data = await sync_to_async(extract_profile_data)(profile)
        return profile_data

    @staticmethod
    async def get_subs(profiles):
        result = []
        for p in profiles:
            profile_obj = await sync_to_async(Profile.objects.get)(user_id=p["user"])
            subscribers_ids = await sync_to_async(list)(profile_obj.subscribers.values_list("id", flat=True))
            subscriptions_ids = await sync_to_async(list)(profile_obj.subscriptions.values_list("id", flat=True))
            p["subscribers"] = subscribers_ids
            p["subscriptions"] = subscriptions_ids
            result.append(p)
        return result

    @staticmethod
    async def post_message(message_data):
        try:
            chat_group = await sync_to_async(ChatGroup.objects.get)(id=message_data.chat_group_id)
            author = await sync_to_async(User.objects.get)(id=message_data.author_id)

            new_message = await sync_to_async(GroupMessage.objects.create)(
                chat_group=chat_group,
                author=author,
                body=message_data.body,
            )

            return new_message

        except ChatGroup.DoesNotExist:
            raise HTTPException(status_code=404, detail="Chat group not found")
        except User.DoesNotExist:
            raise HTTPException(status_code=404, detail="Author not found")

    @staticmethod
    async def post_message_file(chat_group_id: int, author_id: int, file: UploadFile):
        try:
            chat_group = await sync_to_async(ChatGroup.objects.get)(id=chat_group_id)
            author = await sync_to_async(User.objects.get)(id=author_id)

            contents = await file.read()  # читаємо байти файлу
            django_file = SimpleUploadedFile(
                name=file.filename,
                content=contents,
                content_type=file.content_type
            )

            new_message = await sync_to_async(GroupMessage.objects.create)(
                chat_group=chat_group,
                author=author,
                file=django_file,
            )
            return new_message

        except ChatGroup.DoesNotExist:
            raise HTTPException(status_code=404, detail="Chat group not found")
        except User.DoesNotExist:
            raise HTTPException(status_code=404, detail="Author not found")