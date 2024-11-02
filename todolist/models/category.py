from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=40, unique=True)
    # tasks = models.ForeignKey('Task', on_delete=models.PROTECT, related_name='category')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'task_manager_category'
        verbose_name = 'Category'
        unique_together = ('name',)
        ordering = ['name']
        verbose_name_plural = 'categories'
