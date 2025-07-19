from asgiref.sync import async_to_sync
from django.http import Http404, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from channels.layers import  get_channel_layer
from test_django.chat_models import ChatGroup, GroupMessage
from test_django.guard_login import login_required_message
from test_django.forms import ChatMessageForm
from django.contrib.auth.models import User
import uuid


@login_required_message
def chats_view(request, chatroom_name="public-chat"):
    print(f"[DEBUG] chats_view: Отримано chatroom_name -> {chatroom_name}")
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    print(f"[DEBUG] chats_view: ChatGroup знайдено -> {chat_group.group_name}")

    chat_messages = chat_group.chat_messages.all()
    form = ChatMessageForm()

    other_user = None
    if chat_group.is_private:
        if request.user not in chat_group.members.all():
            print(f"[DEBUG] chats_view: Користувач {request.user} не в групі -> {chat_group.group_name}")
            raise Http404()
        for member in chat_group.members.all():
            if member != request.user:
                other_user = member
                break
        print(f"[DEBUG] chats_view: Приватна кімната, інший користувач -> {other_user}")

    if request.method == "POST":
        form = ChatMessageForm(data=request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.author = request.user
            message.chat_group = chat_group
            message.save()
            print(f"[DEBUG] chats_view: Збережено повідомлення -> {message.body}")

            if request.headers.get('HX-Request') == 'true':
                print("[DEBUG] chats_view: HX-Request TRUE — повертаємо partial")
                return render(request, "cooking/component/_chat_message.html",
                              {"message": message, "user": request.user})

            return redirect("chats_view")

    context = {
        "title": "Чат",
        "chat_messages": chat_messages,
        "form": form,
        "other_user": other_user,
        "chatroom_name": chatroom_name,
    }

    print(f"[DEBUG] chats_view: Рендеримо chats_form.html для кімнати -> {chatroom_name}")
    return render(request, "cooking/chats_form.html", context)


@login_required_message
def get_or_create_chat(request, username):
    print(f"[DEBUG] get_or_create_chat: username -> {username}")

    if request.user.username == username:
        print("[DEBUG] get_or_create_chat: спроба створити чат з собою")
        return redirect('home')

    try:
        other_user = User.objects.get(username=username)
        print(f"[DEBUG] get_or_create_chat: Знайдено користувача -> {other_user}")
    except User.DoesNotExist:
        print("[DEBUG] get_or_create_chat: Користувача не знайдено")
        raise Http404("Користувач не знайдений.")

    my_chatrooms = request.user.chat_groups.filter(is_private=True)
    chatroom = None

    if my_chatrooms.exists():
        for cr in my_chatrooms:
            if other_user in cr.members.all():
                chatroom = cr
                print(f"[DEBUG] get_or_create_chat: Знайдено існуючу кімнату -> {chatroom.group_name}")
                break

    if not chatroom:
        group_name = f"private-{uuid.uuid4().hex[:8]}"
        print(f"[DEBUG] get_or_create_chat: Створюємо нову кімнату -> {group_name}")
        chatroom = ChatGroup.objects.create(
            is_private=True,
            group_name=group_name
        )
        chatroom.members.add(other_user, request.user)

    if not chatroom.group_name:
        raise ValueError("Помилка: у чатрума відсутня назва.")

    return redirect('chat_rooms', chatroom_name=chatroom.group_name)


@login_required_message
def my_chats_view(request):
    user = request.user
    chats = user.chat_groups.all()

    return render(request, 'cooking/my_chats.html', {'chats': chats})


def chat_file_upload(request, chatroom_name):
    chat_group = get_object_or_404(ChatGroup, group_name=chatroom_name)
    print(f"[DEBUG] DEBUG CHAT_GROUP DEBUG CHAT_GROUPDEBUG CHAT_GROUPDEBUG CHAT_GROUPDEBUG CHAT_GROUP {chat_group}")
    if request.htmx and request.FILES:
        file = request.FILES["file"]
        message = GroupMessage.objects.create(
            file=file,
            author=request.user,
            chat_group=chat_group,
        )
        channel_layer = get_channel_layer()
        event = {
            "type": "message_handler",
            "message_id": message.id,
        }
        async_to_sync(channel_layer.group_send)(
            chatroom_name, event
        )
    return HttpResponse()



