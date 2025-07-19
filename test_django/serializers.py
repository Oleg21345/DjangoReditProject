from test_django.models import Post, Category
from rest_framework import serializers


class PostSerializers(serializers.ModelSerializer):
    """АПІ мого додатку"""

    class Meta:
        model = Post
        fields = ("id", "title", "category_id", "content", "create_at", "author")


class CategorySerializers(serializers.ModelSerializer):
    """АПІ мого додатку"""

    class Meta:
        model = Category
        fields = ("id","title")

