from django.urls import path, include
from rest_framework import routers

from todolist.views.auth import LoginView, RegisterUserGenericView, RefreshTokenView
from todolist.views.category_views import CategoryViewSet
from todolist.views.tasks_views import *

router = routers.DefaultRouter()
router.register(r'categories', CategoryViewSet)

urlpatterns = [
    path('tasks/', TaskListCreateAPIView.as_view(), name='task_list'),
    path('tasks/<slug:t_slug>/', TaskRetrieveUpdateDestroyAPIView.as_view(), name='task_detail'),
    path('subtasks/', SubTaskListCreateView.as_view(), name='subtask-list-create'),
    path('subtasks/<int:pk>/', SubTaskDetailUpdateDeleteView.as_view(), name='subtask-detail-update-delete'),
    path('categories/', include(router.urls)),  # Убедитесь, что этот путь правильный
    path('login/', LoginView.as_view()),
    path('register/', RegisterUserGenericView.as_view()),
    path('refreshToken/', RefreshTokenView.as_view()),



]















