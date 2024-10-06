from django.db import models


STATUS_CHOICES = [('new', 'New'), ('in_progress', 'In progress'), ('pending', 'Pending'), ('blocked', 'Blocked'), ('done', 'Done'), ]


class Task(models.Model):
    title = models.CharField("unicum title for task", max_length=100, unique=True)
    description = models.TextField('tasks description')
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





















