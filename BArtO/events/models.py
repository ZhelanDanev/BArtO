from typing import TYPE_CHECKING

from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy

from BArtO.accounts.models import AppUser

UserModel = get_user_model()

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractUser


class Event(models.Model):
    title = models.CharField(max_length=255)
    poster = models.ImageField(upload_to='events_poster/', blank=True, null=True)
    description = models.TextField(blank=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True, blank=True)
    location = models.CharField(max_length=255)
    organizer = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='organized_events')
    discussion_enabled = models.BooleanField(default=True)

    def get_absolute_url(self):
        return reverse_lazy('event_details', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title


class EventParticipant(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='participants')
    artist = models.ForeignKey(AppUser, on_delete=models.CASCADE, related_name='events_participated')
    confirmed = models.BooleanField(default=False)


class Comment(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')

    def __str__(self):
        return f"Comment by {self.author.username} on {self.event.title}"
