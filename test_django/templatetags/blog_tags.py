from django import template
from django.db.models import Count
from test_django.models import Category, Post


register = template.Library()


@register.simple_tag()
def get_all_category():
    return Category.objects.annotate(posts_count=Count('posts')).filter(posts__is_published = True)


