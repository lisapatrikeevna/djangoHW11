from django.db import models

from todolist.models.category import Category

STATUS_CHOICES = [('new', 'New'), ('in_progress', 'In progress'), ('pending', 'Pending'), ('blocked', 'Blocked'), ('done', 'Done'), ]


class Task(models.Model):
    title = models.CharField("unicum title for task", max_length=100, unique=True)
    description = models.TextField('tasks description')
    categories = models.ManyToManyField(Category, related_name='tasks', blank=True)
    status = models.CharField('status', choices=STATUS_CHOICES, default='new', max_length=20)
    deadline = models.DateTimeField('deadline')
    created_at = models.DateTimeField('created at', auto_now_add=True)
    objects = models.Manager()

    def __str__(self):
        return self.title

    class Meta:
        # db_table = 'task_manager_task'
        verbose_name = 'Task'
        ordering = ['-created_at']
        unique_together = ('title',)


class SubTask(models.Model):
    title = models.CharField('subTitle', max_length=100)
    description = models.TextField('subDescription')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='subtasks')
    status = models.CharField('status', choices=STATUS_CHOICES, default='new', max_length=20)
    deadline = models.DateTimeField('deadline')
    created_at = models.DateTimeField('created at', auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'task_manager_subtask'
        ordering = ['-created_at']
        verbose_name = 'SubTask'
        unique_together = ('title',)

