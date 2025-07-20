from django.contrib.auth import get_user_model
from test_django.models import Profile
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.cache import cache
from test_django.models import Post, Comment

User = get_user_model()

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)




@receiver(post_save, sender=Post)
@receiver(post_delete, sender=Post)
def clear_post_cache(sender, instance, **kwargs):
    cache.delete(f'post_detail_post_{instance.pk}')
    cache.delete('post_detail_ext_post')

@receiver(post_save, sender=Comment)
@receiver(post_delete, sender=Comment)
def clear_comments_cache(sender, instance, **kwargs):
    post_pk = instance.post.pk
    cache.delete(f'post_detail_comments_{post_pk}')
