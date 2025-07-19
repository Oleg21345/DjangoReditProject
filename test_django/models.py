from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User



class Category(models.Model):

    title = models.CharField(max_length=255, verbose_name="Заголовок")

    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("category_post", kwargs={"pk": self.pk})

    def get_absolute_url_author(self, user_id):
        return reverse('category_post_author', kwargs={'user_id': user_id, 'category_id': self.pk})

    class Meta:
        verbose_name = "Категорія"
        verbose_name_plural = "Категорії"

class Post(models.Model):

    title = models.CharField(max_length=255, verbose_name="Заголовок")
    content = models.TextField(max_length=1000, default="Поки що тут нічого немає", verbose_name="Текст статті")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    update_at = models.DateTimeField(auto_now=True, verbose_name="Дата оновлення")
    image = models.ImageField(upload_to="photos/", null=True, verbose_name="Картинка")
    watched = models.IntegerField(default=0, verbose_name="Перегляди")
    is_published = models.BooleanField(default=True, verbose_name="Публікація")
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE,related_name="posts" , verbose_name="Категорія")
    author = models.ForeignKey(User, default=None, null=True, blank=False, on_delete=models.CASCADE)


    def __str__(self):
        return f"{self.title}"

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

    def get_absolute_url_author(self):
        return reverse("author_posts", kwargs={"pk": self.author.pk})

    class Meta:
        verbose_name = "Пост"
        verbose_name_plural = "Пости"

    @property
    def like_count(self):
        return self.votes.filter(value=1).count()

    @property
    def dislike_count(self):
        return self.votes.filter(value=-1).count()


class Vote(models.Model):
    VOTE_CHOICES = (
        (1, 'Like'),
        (-1, 'Dislike'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='votes')
    value = models.SmallIntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('user', 'post')



class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name="Пост")
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Користувач")
    reply_to_comment = models.ForeignKey("self", on_delete=models.CASCADE, blank=True, null=True)
    text = models.TextField(verbose_name="Коментарій")
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    @property
    def like_count(self):
        return self.votes.filter(value=1).count()

    @property
    def dislike_count(self):
        return self.votes.filter(value=-1).count()


    def __str__(self):
        return self.text

    class Meta:
        verbose_name = "Коментарій"
        verbose_name_plural = "Коментарії"


class VoteForComment(models.Model):
    VOTE_CHOICES = (
        (1, 'Like'),
        (-1, 'Dislike'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='votes')
    value = models.SmallIntegerField(choices=VOTE_CHOICES)

    class Meta:
        unique_together = ('user', 'comment')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    subscribers = models.ManyToManyField(User, related_name="following", blank=True)
    subscriptions = models.ManyToManyField(User, related_name="follow", blank=True)
    avatars = models.ImageField(upload_to='avatars/', blank=True, null=True, default="photos/Goroshek.png")


class Notificated(models.Model):
    user = models.ForeignKey(User, related_name="user_notif", on_delete=models.CASCADE)
    notificated = models.TextField()
    from_user = models.ForeignKey(User, related_name="sent_notifications", null=True, blank=True, on_delete=models.SET_NULL)
    is_read = models.BooleanField(default=False)
    notificated_count = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    def __str__(self):
        return f"Notification for {self.user.username}: {self.notificated[:20]}"

