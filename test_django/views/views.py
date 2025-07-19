from django.db.models import F, Q, Count
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView
from django.urls import reverse_lazy
from test_django.forms import PostAddForm, CommentForm, UserChangePassForm, CategoryAddForm
from test_django.guard_login import login_required_message
from test_django.models import Post, Category, Comment, Profile, Notificated
from test_django.add_not import add_notification
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordChangeView
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from test_django.forms import ProfileForm
from django.shortcuts import  redirect
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.utils import timezone

# Create your views here.

# category = Category.objects.get(pk=4)
# category.posts.all()
# <QuerySet []>


class Home(ListView): # Тут краще робити через клас так як коротше

    model = Post
    context_object_name = "posts"
    template_name = "cooking/index.html"
    extra_context = {"title": "Головна сторінка"}


class AuthorPostsView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'cooking/posts_by_author.html'

    def get_queryset(self):
        self.author = get_object_or_404(User, pk=self.kwargs['user_id'])
        return Post.objects.filter(author=self.author)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['author'] = self.author

        categories = Category.objects.annotate(
            posts_count=Count('posts', filter=Q(posts__author=self.author))
        ).filter(posts_count__gt=0)

        context['categories'] = categories
        return context


class AuthorCategoryPostsView(ListView):
    model = Post
    context_object_name = "posts"
    template_name = "cooking/posts_by_author.html"

    def get_queryset(self):
        self.author = get_object_or_404(User, pk=self.kwargs["user_id"])
        self.category = get_object_or_404(Category, pk=self.kwargs["category_id"])
        return Post.objects.filter(
            author=self.author,
            category_id=self.category,
            is_published=True
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["author"] = self.author
        context["category"] = self.category
        context["title"] = f"Статті автора {self.author.username} в категорії {self.category.title}"

        context["categories"] = Category.objects.annotate(
            posts_count=Count('posts', filter=Q(posts__author=self.author))
        ).filter(posts_count__gt=0)

        return context



class CategoryPost(Home):

    def get_queryset(self):
        return Post.objects.filter(category_id=self.kwargs["pk"], is_published=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        category = Category.objects.get(pk=self.kwargs["pk"])
        context["title"] = category.title
        return context


class PostDetail(DetailView):
    model = Post
    template_name = "cooking/articaldetail.html"

    def get_queryset(self):
        """Фільтрація"""
        return Post.objects.filter(pk=self.kwargs["pk"])

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        Post.objects.filter(pk=self.kwargs["pk"]).update(watched=F("watched") + 1)
        ext_post = Post.objects.all().exclude(pk=self.kwargs["pk"]).order_by("-watched")[:5]
        post = Post.objects.get(pk=self.kwargs["pk"])
        context["title"] = post.title
        context["ext_post"] = ext_post
        context["comments"] = Comment.objects.filter(post=post)
        if self.request.user.is_authenticated:
            context["comment_form"] = CommentForm

        edit_comment_id = self.request.GET.get("edit")
        if edit_comment_id:
            try:
                edit_comment_id = int(edit_comment_id)
            except ValueError:
                edit_comment_id = None
        context["edit_comment_id"] = edit_comment_id

        reply_comment_id = self.request.GET.get("reply")
        if reply_comment_id:
            try:
                reply_comment_id = int(reply_comment_id)
            except ValueError:
                reply_comment_id = None
        context["reply_to_comment_id"] = reply_comment_id

        return context

    def post(self, request, *args, **kwargs):
        post = self.get_object()

        comment_id = request.POST.get("comment_id")
        if comment_id:
            comment = get_object_or_404(Comment, pk=comment_id, user=request.user)
            new_text = request.POST.get("text", "").strip()
            if new_text:
                comment.text = new_text
                comment.save()
                return redirect("post_detail", pk=post.pk)
            else:
                context = self.get_context_data()
                context["edit_comment_id"] = comment.id
                context["comment_form"] = CommentForm(instance=comment)
                return self.render_to_response(context)

        form = CommentForm(request.POST)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            new_comment.save()
            return redirect("post_detail", pk=post.pk)

        context = self.get_context_data()
        context["comment_form"] = form
        return self.render_to_response(context)


class AddPost(CreateView):
    """Додавання посту через клас"""
    form_class = PostAddForm
    template_name = "cooking/artical_add_form.html"
    extra_context = {"title": "Додати статтю"}

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class AddCategory(CreateView):
    """Додавання нової категорії"""
    form_class = CategoryAddForm
    template_name = "cooking/category_add_form.html"
    extra_context = {"title": "Додати категорію"}
    success_url = reverse_lazy("add")


class PostUpdate(UpdateView):
    """Оновлювати пости"""
    model = Post
    form_class = PostAddForm
    template_name = "cooking/artical_add_form.html"
    extra_context = {"title": "Оновити статью"}

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse_lazy("home")


class PostDelete(DeleteView):
    """Видалення статті"""
    model = Post
    success_url = reverse_lazy("home")
    context_object_name = "post"
    template_name = "cooking/post_confirm_delete.html"
    extra_context = {"title": "Видалення статті"}

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse_lazy("home")


class CommentDelete(DeleteView):
    """Видалення коментаря"""
    model = Comment
    success_url = reverse_lazy("post_detail")
    context_object_name = "comment"
    template_name = "cooking/comment_confirm_delete.html"
    extra_context = {"title": "Видалення коментаря"}

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse_lazy("post_detail", kwargs={"pk": self.object.post.pk})


class CommentUpdate(UpdateView):
    """Оновлювати коментар"""
    model = Comment
    form_class = CommentForm
    template_name = "cooking/artical_add_form.html"
    extra_context = {"title": "Оновити коментар"}

    def get_success_url(self):
        next_url = self.request.GET.get("next")
        if next_url:
            return next_url
        return reverse_lazy("post_detail", kwargs={"pk": self.object.post.pk})


class SearchResults(Home):
    """Клас для пошуку статті"""

    def get_queryset(self):
        """Фільтрація"""
        word = self.request.GET.get("q")
        posts = Post.objects.filter(
            Q(title__icontains=word) | Q(content__icontains=word)
        )
        return posts


class UserChangePass(PasswordChangeView):
    """Зміна пароля"""
    form_class = UserChangePassForm
    success_url = reverse_lazy("home")
    template_name = "cooking/change_password.html"


def add_comment(request, post_id):
    """Додавання коментаря"""
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.user = request.user
        comment.post = Post.objects.get(pk=post_id)
        comment.save()
        messages.success(request, "Коментарій був успішно доданий")
        
    return redirect("post_detail", post_id)


def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    posts = Post.objects.filter(author=user)
    subs = user.profile.subscribers.count()
    subscriptions = user.profile.subscriptions.count()
    count_post = posts.count()

    user_profile = Profile.objects.get(user=user)

    is_following = user_profile.subscribers.filter(pk=request.user.pk).exists()
    context = {
        "user": user,
        "posts": posts,
        "subs": subs,
        "subscriptions": subscriptions,
        "is_following": is_following,
        "count_post": count_post,
    }
    return render(request, "cooking/profile.html", context)


def follow_user(request, user_id):
    if request.method == "POST":
        current_user = request.user
        user_follow = User.objects.get(pk=user_id)

        profile_follow = Profile.objects.get(user=user_follow)

        count=0
        count+=1
        add_notification(
            user=user_follow,
            from_user=current_user,
            message="підписався на вас.",
            not_count=1
        )

        current_user_profile = Profile.objects.get(user=current_user)

        profile_follow.subscribers.add(current_user)
        current_user_profile.subscriptions.add(user_follow)

        return redirect('profile', user_id=user_id)

    return redirect('profile', user_id=user_id)


def unfollow_user(request, user_id):
    if request.method == "POST":
        current_user = request.user
        user_unfollow = User.objects.get(pk=user_id)

        profile_unfollow = Profile.objects.get(user=user_unfollow)
        current_user_profile = Profile.objects.get(user=current_user)

        profile_unfollow.subscribers.remove(current_user)
        current_user_profile.subscriptions.remove(user_unfollow)

        return redirect('profile', user_id=user_id)

    return redirect('profile', user_id=user_id)


def user_detail_list(request, pk, view_type):
    user = User.objects.get(pk=pk)
    profile = user.profile
    subs = profile.subscribers.count()
    subscriptions = profile.subscriptions.count()
    posts = Post.objects.filter(author=user)
    count_post = posts.count()

    if view_type == "subscribers":
        data = profile.subscribers.all()
        template = "cooking/subscriptions_list.html"
    elif view_type == "subscriptions":
        data = profile.subscriptions.all()
        template = "cooking/subscribers.html"
    elif view_type == "posts":
        data = posts
        template = "cooking/posts_list.html"
    else:
        return redirect("profile", user_id=pk)

    context = {
        "user": user,
        "posts": posts,
        "data": data,
        "subs": subs,
        "subscriptions": subscriptions,
        "count_post": count_post,
    }

    return render(request, template, context)


def changeprofile(request):
    profile = request.user.profile
    if request.method == 'POST':
        profile_form = ProfileForm(request.POST, request.FILES, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            return HttpResponseRedirect(reverse('profile', kwargs={'user_id': request.user.pk}))
    else:
        profile_form = ProfileForm(instance=profile)

    return render(request, 'login/change.html', {
        'form': profile_form,
        'user': request.user
    })


@login_required_message
def save_avatar(request, user_id):
    if request.method == "POST" and request.FILES.get("avatars"):
        if request.user.id == user_id:
            profile = request.user.profile
            profile.avatars = request.FILES["avatars"]
            profile.save()
    return redirect("profile", user_id=user_id)



@login_required_message
def reply_to_comment(request, post_id):
    if request.method == "POST":
        post = get_object_or_404(Post, pk=post_id)
        reply_comment_id = request.POST.get("reply_to_comment")
        form = CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.user = request.user
            if reply_comment_id:
                parent_comment = get_object_or_404(Comment, pk=reply_comment_id)
                new_comment.reply_to_comment = parent_comment
            new_comment.save()

            if request.headers.get("x-requested-with") == "XMLHttpRequest":
                data = {
                    "id": new_comment.id,
                    "text": new_comment.text,
                    "user": new_comment.user.username,
                    "user_avatar": new_comment.user.profile.avatars.url if new_comment.user.profile.avatars else "https://www.pngall.com/wp-content/uploads/12/Avatar-Profile-PNG-Photos.png",
                    "created": new_comment.create_at.strftime("%d.%m.%Y %H:%M"),
                    "reply_to_comment_id": reply_comment_id,
                }
                return JsonResponse(data)

            return redirect("post_detail", pk=post.pk)

        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            return JsonResponse({"error": "Invalid form data"}, status=400)

        return redirect("post_detail", pk=post.pk)

    return redirect("post_detail", pk=post_id)


@login_required_message
def notificated_view(request):
    notifications = request.user.user_notif.order_by('-create_at')
    unread_count = request.user.user_notif.filter(is_read=False).count()

    context = {
        'notifications': notifications,
        'unread_count': unread_count,
    }
    return render(request, 'cooking/notifications.html', context)


@login_required_message
def mark_notificated_as_read(request):
    request.user.user_notif.filter(is_read=False).update(is_read=True)
    return redirect('notificated')











































































































