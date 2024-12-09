
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse_lazy

from BArtO.accounts.managers import AppUserManager


class AppUser(AbstractUser):
    email = models.EmailField(unique=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    role = models.CharField(
        max_length=20,
        choices=[
            ('artist', 'Artist'),
            ('editor', 'Editor'),
            ('admin', 'Admin'),
        ],
        default='artist',
    )
    social_media_links = models.JSONField(blank=True, null=True)

    USERNAME_FIELD = 'username'
    objects = AppUserManager()

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"


UserModel = get_user_model()


class Artist(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name="artist")
    first_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    category = models.CharField(max_length=20, choices=[
        ('musician', 'Музикант'),
        ('writer', 'Писател'),
        ('actor', 'Актьор'),
    ])

    def delete(self, using=None, keep_parents=False):
        """
        Презаписва метода за изтриване, за да изтрие и свързания User.
        """
        user = self.user
        user.delete()
        super().delete(using=keep_parents)

