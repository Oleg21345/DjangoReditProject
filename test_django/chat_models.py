import os.path
from PIL import Image
from django.db import models
from django.contrib.auth.models import User
import shortuuid
import mimetypes

class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128, unique=True, default=shortuuid.uuid)
    users_online = models.ManyToManyField(User, related_name="online_is_group", blank=True, default=shortuuid.uuid)
    members = models.ManyToManyField(User, related_name="chat_groups", blank=True)
    is_private = models.BooleanField(default=False)

    def __str__(self):
        return self.group_name


class GroupMessage(models.Model):

    chat_group = models.ForeignKey(ChatGroup, related_name="chat_messages", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=300, blank=True, null=True)
    file = models.FileField(upload_to="photos/", blank=True, null=False)
    create_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")

    @property
    def filename(self):
        if self.file:
            return os.path.basename(self.file.name)
        else:
            return None

    def __str__(self):
        if self.body:
            return f"{self.author} : {self.body}"
        else:
            return f"{self.author} : {self.filename}"

    class Meta:
        ordering = ["-create_at"]

    @property
    def mime_type(self):
        if self.file:
            mime, _ = mimetypes.guess_type(self.file.name)
            return mime
        return None

    @property
    def is_image(self):
        mime = self.mime_type
        return mime is not None and mime.startswith('image/')

    @property
    def is_pdf(self):
        return self.mime_type == 'application/pdf'

    @property
    def is_text(self):
        return self.mime_type == 'text/plain'

    @property
    def is_mp4(self):
        return self.mime_type == 'video/mp4'

    @property
    def is_webm(self):
        return self.mime_type == 'video/webm'

    @property
    def is_mpg(self):
        return self.mime_type == 'video/mpeg'










