from test_django.models import Comment, VoteForComment
from django.shortcuts import get_object_or_404, redirect
from test_django.guard_login import login_required_message
from test_django.add_not import add_notification

def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    vote, created = VoteForComment.objects.get_or_create(user=request.user, comment=comment)

    if vote.value == 1:
        vote.delete()
        vote.save()
    else:
        vote.value = 1
        vote.save()

    return redirect('post_detail', pk=pk)

def dislike_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    vote, created = VoteForComment.objects.get_or_create(user=request.user, comment=comment)


    if vote.value == -1:
        vote.delete()
        vote.save()
    else:
        vote.value = -1
        vote.save()

    return redirect('post_detail', pk=pk)


@login_required_message
def vote_comment(request, pk, value):
    comment = get_object_or_404(Comment, pk=pk)
    user = request.user

    if value not in ['1', '-1']:
        return redirect('post_detail', pk=comment.post.pk)

    value = int(value)

    try:
        vote = VoteForComment.objects.get(user=user, comment=comment)

        if vote.value == value:
            vote.delete()
        else:
            vote.value = value
            vote.save()
    except VoteForComment.DoesNotExist:
        VoteForComment.objects.create(user=user, comment=comment, value=value)

    if comment.user != user:
        action = "лайкнув" if value == 1 else "дизлайкнув"
        add_notification(
            user=comment.user,
            from_user=user,
            message=f"{action} ваш коментар.",
            not_count=1
        )

    return redirect('post_detail', pk=comment.post.pk)
