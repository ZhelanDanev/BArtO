from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse

UserModel = get_user_model()


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
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user} - {self.notification_type}"

    def get_absolute_url(self):
        if self.notification_type in {self.FOLLOW, self.UNFOLLOW}:
            return reverse('artist_details', args=[self.sender.id])
        elif self.notification_type == self.EVENT_INVITE:
            return reverse('event_details', args=[self.event.id])
        return '#'



# class EventInvitation(models.Model):
#     event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="invitations")  # Връзка към Event
#     invited_user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="event_invitations")
#     is_accepted = models.BooleanField(default=False)
#     is_read = models.BooleanField(default=False)
#     invited_at = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return f"Invitation to {self.event.title} for {self.invited_user.username}"
