from rest_framework.serializers import ModelSerializer

from todolist.models import Task


class TasksSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
