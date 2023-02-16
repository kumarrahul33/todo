from django.urls import path
from todo_manager import views

urlpatterns = [
    path('tasks/', views.task_list),
    path('tasks/<int:pk>/', views.task_detail),
    path('mark_done/<int:pk>/', views.mark_done),
]