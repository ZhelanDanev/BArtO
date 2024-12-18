
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include

from BArtO.accounts.views import ArtistRegisterView, logout_view, artist_edit, ArtistDeleteView, \
    ArtistDetailView, artist_list

urlpatterns = [
    path('register/', ArtistRegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', logout_view, name='logout'),
    path('artists/', artist_list, name='artist_list'),
    path('profile/<int:pk>/', ArtistDetailView.as_view(), name='artist_details'),  # Профилът
    path('profile/<int:pk>/edit/', artist_edit, name='artist_edit'),    # Редакция
    path('profile/<int:pk>/delete/', ArtistDeleteView.as_view(), name='artist_delete'),  # Изтриване
]
