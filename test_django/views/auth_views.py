from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib import messages
from test_django.forms import  LoginForm, RegisterForm, EmailChangePassword
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetView

def user_login(request):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request ,user)
            messages.success(request, message="Ви успішно увійшли в акаунт")
            return redirect("home")
    else:
        form = LoginForm()

    context = {
        "title": "Авторизація користувача",
        "form": form
    }
    return render(request, "cooking/login_form.html", context)


# def reset_password(request):
#     if request.method == "POST":
#         form = EmailChangePassword(data=request.POST)
#         if form.is_valid():
#             email_in_form = form.cleaned_data["email"]
#             email_user = User.objects.filter(email=email_in_form)
#             if email_user:
#                 messages.info(request, message="На вашу пошту надійшов код, впишіть його в форму")
#                 return redirect("code")
#             else:
#                 messages.error(request, "Помилка, акаунт з такими даними не був знайдений")
#         else:
#             form = EmailChangePassword()
#
#         context = {
#             "title": "Зміна паролю",
#             "form": form
#         }
#         return render(request, "cooking/reset_password.html", context)

def user_logout(request):
    logout(request)
    messages.success(request, message="Ви успішно вийшли з акаунту")
    return redirect("home")


def register_user(request):
    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, message="Ви успішно увійшли в акаунт")
            return redirect("login_user")
    else:
        form = RegisterForm()

    context = {
        "title": "Реєстрація користувача",
        "form": form
    }
    return render(request, "cooking/register_form.html", context)


class ResetPasswordEmail(PasswordResetView):
    """"""

