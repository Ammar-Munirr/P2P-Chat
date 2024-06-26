from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class MyChat(models.Model):
    me = models.ForeignKey(User, on_delete=models.CASCADE, related_name="me")
    frnd = models.ForeignKey(User, on_delete=models.CASCADE, related_name="frnd")
    chat = models.JSONField(default=dict)
