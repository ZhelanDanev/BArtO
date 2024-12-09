from django.urls import path
from .views import NewsListView, NewsDetailView, AddCommentView, create_news, edit_news, delete_news

app_name = 'news'

urlpatterns = [
    path("", NewsListView.as_view(), name="news_list"),
    path('create/', create_news, name='create_news'),
    path("<int:pk>/", NewsDetailView.as_view(), name="news_detail"),
    path('edit/<int:pk>/', edit_news, name='edit_news'),  # Редактиране на новина
    path('delete/<int:pk>/', delete_news, name='delete_news'),  # Изтриване на новина
    path("<int:pk>/add_comment/", AddCommentView.as_view(), name="add_comment"),
]

