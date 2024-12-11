from django.urls import path
from .views import work_list, work_detail, work_create, work_delete

urlpatterns = [
    path('', work_list, name='work_list'),
    path('create/', work_create, name='work_create'),
    path('<int:pk>/', work_detail, name='work_detail'),
    path('<int:pk>/delete/', work_delete, name='work_delete')
]
