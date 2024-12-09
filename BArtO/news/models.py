from django.contrib.auth import get_user_model
from django.db import models
from django.conf import settings
from django.urls import reverse

UserModel = get_user_model()


class News(models.Model):
    author = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name="news")
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("news:news_detail", args=[str(self.id)])


class NewsComment(models.Model):
    news = models.ForeignKey(News, on_delete=models.CASCADE, related_name="comments")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.news.title}"
