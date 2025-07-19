from test_django.models import Notificated
from django.contrib.auth.models import User

# def add_notification(user: User, message: str, not_count):
#     Notificated.objects.create(user=user, notificated=message, notificated_count=not_count)
#
def add_notification(user: User, from_user, message, not_count=1):
    Notificated.objects.create(
        user=user,
        from_user=from_user,
        notificated=message,
        notificated_count=not_count,
    )
