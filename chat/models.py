from django.db import models
from users.models import CustomUser


class CustomerChat(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chats_sent')
    other_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='chats_received')
    message = models.TextField(null=True, blank=True)
    group_name = models.CharField(max_length=50, null=True, blank=True)
    time = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    from_user = models.BooleanField(default=False)