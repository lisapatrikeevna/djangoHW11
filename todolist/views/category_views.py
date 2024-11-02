from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets

from todolist.models.category import Category
from todolist.serializers.task import CategoryCreateSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategoryCreateSerializer

    # def get_queryset(self):
    #     return super().get_queryset()

    @action(detail=True, methods=['get'], url_path='count_tasks')
    def count_tasks(self, request,pk=None):
        category = self.get_object()  # Получаем категорию по ID
        task_count = category.tasks.count()  # Подсчитываем связанные задачи

        return Response({'category': category.name, 'task_count': task_count})
