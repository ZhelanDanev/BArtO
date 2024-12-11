from django.contrib.auth import get_user_model
from django.db import models

UserModel = get_user_model()


class Work(models.Model):
    CATEGORY_CHOICES = [
        ('music', 'Music'),
        ('writing', 'Writing'),
        ('acting', 'Acting'),
    ]

    author = models.ForeignKey(
        UserModel,
        on_delete=models.CASCADE,
        related_name='works'
    )
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    genre = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    youtube_link = models.URLField(blank=True, null=True)
    audio_file = models.FileField(upload_to='audio/', blank=True, null=True)
    text_content = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
