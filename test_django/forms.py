from django import forms
from test_django.models import Post, Comment, Category, Profile
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm
from test_django.chat_models import GroupMessage

class PostAddForm(forms.ModelForm):

    class Meta:

        model = Post
        fields = ("title", "content", "image", "category_id")

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control"
            }),
            "content": forms.Textarea(attrs={
                "class": "form-control"
            }),
            "image": forms.FileInput(attrs={
                "class": "form-control"
            }),
            "category_id": forms.Select(attrs={
                "class": "form-control"
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        category = Category.objects.last()
        if category:
            self.fields["category_id"].initial = category.id


class CategoryAddForm(forms.ModelForm):

    class Meta:
        model = Category
        fields = ("title",)

        widgets = {
            "title": forms.TextInput(attrs={
                "class": "form-control"
            })
        }


class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Ім'я користувача",
        max_length=80,
        widget=forms.TextInput(attrs={
            "class": "form-control"
        })
    )

    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            "class": "form-control"
        })
    )


class RegisterForm(UserCreationForm):

    class Meta:
        model = User
        fields = (
            "username",
            "email",
            "password1",
            "password2"
        )

    username = forms.CharField(
        max_length=80,
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Ім'я користувача"
        })
    )

    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Електрона пошта"
        })
    )

    password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Пароль"
        })
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Повторити пароль"
        })
    )


class CommentForm(forms.ModelForm):
    """Форма під коментарі"""

    class Meta:
        model = Comment
        fields = ("text",)

        widgets = {
            "text": forms.TextInput(attrs={
                "class": "form-control",
                "placeholder": "Додати коментар"
            })
        }


class EmailChangePassword(forms.ModelForm):
    """Змінна пароля якщо користувач забув його"""
    email = forms.CharField(
        label="Електрона адреса або ім'я користувача",
        widget=forms.TextInput(attrs={
            "class": "form-control"
        })
    )


class UserChangePassForm(PasswordChangeForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({
                "class": "form-control py-2 px-3",
                "style": "border-radius: 8px;"
            })


class ProfileForm(forms.ModelForm):

    avatar = forms.ImageField(label='', widget=forms.FileInput)

    class Meta:
        model = Profile
        fields = ["avatars"]



class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = GroupMessage
        fields = ["body"]
        widgets = {
            "body": forms.TextInput(attrs={
                "class": "form-control rounded-3 px-3 py-2",
                "placeholder": "Додати повідомлення...",
                "autocomplete": "off",
                "style": "width: 100%; box-shadow: none;"
            })
        }

