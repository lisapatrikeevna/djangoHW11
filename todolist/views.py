from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.pagination import PageNumberPagination
from rest_framework.request import Request
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter

from todolist.models import Task
from todolist.serializers.task import TasksSerializer, SubTaskCreateSerializer, TaskCreateSerializer, TaskDetailSerializer


class TaskListCreateAPIView(ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskCreateSerializer
    pagination_class=PageNumberPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['title', 'publisher', 'status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at',]


class TaskRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskDetailSerializer
    lookup_field = 't_slug'


class SubTaskListCreateView(ListCreateAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['status', 'deadline']
    search_fields = ['title', 'description']
    ordering_fields = ['created_at']
    pagination_class = PageNumberPagination


class SubTaskDetailUpdateDeleteView(RetrieveUpdateDestroyAPIView):
    queryset = SubTask.objects.all()
    serializer_class = SubTaskCreateSerializer

    def get_queryset(self):
        return SubTask.objects.filter(active=True)


# @api_view(['GET', 'PUT', 'DELETE'])
# def taskGPD(request: Request, pk: int) -> Response:
#     task = get_object_or_404(Task, id=pk)
#     if request.method == 'GET':
#         res = TasksSerializer(task, context={'request': request})
#         return Response({'data': res.data}, status=status.HTTP_200_OK)  # task_id = request.GET.get('id')  # task_name = request.GET.get('name')  # if pk:  #     task = Task.objects.get(id=pk)  # elif task_name:  #     task = Task.objects.get(name=task_name)  # else:  #     task = Task.objects.all()  # res = TasksSerializer(task, context={'request': request})  # return Response({'data': res.data}, status=status.HTTP_200_OK)
#     if request.method == 'PUT':
#         res = TasksSerializer(task, data=request.data)
#         if res.is_valid():
#             res.save()
#             return Response("Task successfully updated", status=status.HTTP_200_OK)
#         return Response(res.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     if request.method == 'DELETE':
#         task.delete()
#         return Response("Task successfully deleted", status=status.HTTP_200_OK)

# lookup_field
# @api_view(['GET', 'POST'])
# def tasks(request: Request) -> Response:
#     if request.method == 'GET':
#         task = Task.objects.all()
#         pagination = Paginator(task, 10)
#         count_pages = pagination.num_pages
#         page_num = request.GET.get('page', 1)
#         page_data = pagination.get_page(page_num)
#         res = TasksSerializer(page_data, context={'request': request}, many=True)
#         return Response({'data': res.data, 'total_pages': count_pages, 'current_page': page_num}, status=status.HTTP_200_OK)
#     if request.method == 'POST':
#         res = TasksSerializer(data=request.data)
#         if res.is_valid():
#             res.save()
#             return Response("Task successfully created", status=status.HTTP_201_CREATED)
#         return Response(res.errors, status=status.HTTP_400_BAD_REQUEST)














