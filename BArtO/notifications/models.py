from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

UserModel = get_user_model()


from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError
from django.urls import reverse
from BArtO.accounts.models import UserModel  # Update import to your User model


class Notification(models.Model):
    FOLLOW = 'follow'
    UNFOLLOW = 'unfollow'
    EVENT_INVITE = 'event_invite'
    EVENT_CONFIRMATION = 'event_confirmation'

    NOTIFICATION_TYPES = [
        (FOLLOW, 'New Follower'),
        (UNFOLLOW, 'Unfollowed'),
        (EVENT_INVITE, 'Event Invitation'),
        (EVENT_CONFIRMATION, 'Event Confirmation'),
    ]

    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='notifications')
    sender = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='notifications_sent', null=True, blank=True)
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    event = models.ForeignKey('events.Event', on_delete=models.CASCADE, null=True, blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    related_object = GenericForeignKey('content_type', 'object_id')

    def clean(self):
        if self.event and (self.content_type or self.object_id):
            raise ValidationError("Cannot set both 'event' and generic relation fields.")

    def save(self, *args, **kwargs):
        if not self.message:
            if self.notification_type == self.FOLLOW:
                self.message = f"{self.sender.username} is now following you!"
            elif self.notification_type == self.EVENT_INVITE and self.event:
                self.message = f"You have been invited to the event: {self.event.title}"
        super().save(*args, **kwargs)

    def get_target_url(self):
        if self.content_type and self.related_object:
            try:
                return self.related_object.get_absolute_url()
            except AttributeError:
                return None
        elif self.event:
            return reverse('event_details', args=[self.event.id])
        return "#"

    def __str__(self):
        return f"Notification for {self.user} - {self.notification_type}"


# class EventInvitation(models.Model):
#     event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="invitations")  # Връзка към Event
#     invited_user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="event_invitations")
#     is_accepted = models.BooleanField(default=False)
#     is_read = models.BooleanField(default=False)
#     invited_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"Invitation to {self.event.title} for {self.invited_user.username}"
