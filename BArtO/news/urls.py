from django.urls import path
from .views import NewsListView, create_news, edit_news, delete_news, news_detail

app_name = 'news'

urlpatterns = [
    path("", NewsListView.as_view(), name="news_list"),
    path('create/', create_news, name='create_news'),
    path("<int:pk>/", news_detail, name="news_detail"),
    path('edit/<int:pk>/', edit_news, name='edit_news'),
    path('delete/<int:pk>/', delete_news, name='delete_news'),
]

