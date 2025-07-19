from test_django.models import Post
from django.shortcuts import get_object_or_404, redirect
from test_django.models import Vote
from django.contrib.auth.decorators import login_required
from test_django.guard_login import login_required_message
from test_django.add_not import add_notification

def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    vote, created = Vote.objects.get_or_create(user=request.user, post=post)

    if vote.value == 1:
        vote.delete()
        vote.save()
    else:
        vote.value = 1
        vote.save()

    return redirect('post_detail', pk=pk)

def dislike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    vote, created = Vote.objects.get_or_create(user=request.user, post=post)

    if vote.value == -1:
        vote.delete()
        vote.save()
    else:
        vote.value = -1
        vote.save()

    return redirect('post_detail', pk=pk)


@login_required_message
def vote_post(request, pk, value):
    post = get_object_or_404(Post, pk=pk)
    user = request.user

    if value not in ['1', '-1']:
        return redirect('post_detail', pk=pk)

    value = int(value)

    try:
        vote = Vote.objects.get(user=user, post=post)

        if vote.value == value:
            vote.delete()
        else:
            vote.value = value
            vote.save()
    except Vote.DoesNotExist:
        Vote.objects.create(user=user, post=post, value=value)

    if post.author != user:
        action = "лайкнув" if value == 1 else "дизлайкнув"
        add_notification(
            user=post.author,
            from_user=user,
            message=f"{action} ваш пост.",
            not_count=1
        )

    return redirect('post_detail', pk=pk)

