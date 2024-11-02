from datetime import datetime
from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from todolist.models import Task
from todolist.models.category import Category


class TasksSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'


class SubTaskCreateSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['created_at', ]


class CategoryCreateSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

        def create(self, validated_data):
            name = validated_data.get('name')
            if Category.objects.filter(name=name).exists():
                raise ValidationError({"name": "Category with this name already exists."})

            return super().create(validated_data)

        def update(self,instance,validated_data):
            name = validated_data.get('name',instance.name)
            if Category.objects.filter(name=name).exclude(id=instance.id).exists():
                raise ValidationError({"name": "Category with this name already exists."})

            return super().update(instance, validated_data)


class TaskDetailSerializer(ModelSerializer):
    innerTasks = SubTaskCreateSerializer(many=True, read_only=True)
    class Meta:
        model = Task
        fields = '__all__'


class TaskCreateSerializer(ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def validate_deadline(self, value):
        if value < datetime.today().date():
            raise ValidationError("Deadline cannot be in the past.")
        return value

    def create(self, validated_data):
        return super().create(validated_data)






















