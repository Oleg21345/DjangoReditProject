from test_django.serializers import PostSerializers, CategorySerializers
from rest_framework.generics import ListAPIView, RetrieveAPIView
from test_django.models import Post, Category
from rest_framework.permissions import IsAuthenticated


class MarketApi(ListAPIView):
    """Видача всіх статей по апі"""
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializers


class MarketDetailApi(RetrieveAPIView):
    """Видача всіх статей по апі"""
    queryset = Post.objects.filter(is_published=True)
    serializer_class = PostSerializers
    permission_classes = (IsAuthenticated,)

class MarketApiCategory(ListAPIView):
    """Видача всіх статей по апі"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializers

class MarketDetailApiCategory(RetrieveAPIView):
    """Видача всіх статей по апі"""
    queryset = Category.objects.all()
    serializer_class = CategorySerializers


class MarketCategorypost(RetrieveAPIView):
    """Видача всіх статей по апі"""
    queryset = Post.objects.filter(is_published=True)
    serializer_class = CategorySerializers


