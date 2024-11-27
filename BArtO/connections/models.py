from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings

UserModel = get_user_model()


class Connection(models.Model):
    FOLLOW = 'follow'
    COLLABORATE = 'collaborate'

    CONNECTION_TYPES = [
        (FOLLOW, 'Следване'),
        (COLLABORATE, 'Сътрудничество'),
    ]

    from_user = models.ForeignKey(
        UserModel,
        related_name="connections_sent",
        on_delete=models.CASCADE,
    )
    to_user = models.ForeignKey(
        UserModel,
        related_name="connections_received",
        on_delete=models.CASCADE,
    )
    connection_type = models.CharField(
        max_length=20,
        choices=CONNECTION_TYPES,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('from_user', 'to_user', 'connection_type')

    def __str__(self):
        return f"{self.from_user} -> {self.to_user} ({self.get_connection_type_display()})"


class Message(models.Model):
    sender = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content[:20]}"
