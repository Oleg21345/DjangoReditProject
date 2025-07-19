from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps

def login_required_message(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, "Щоб проголосувати, будь ласка, увійдіть або зареєструйтесь.")
            return redirect('login_user')
        return view_func(request, *args, **kwargs)
    return wrapper