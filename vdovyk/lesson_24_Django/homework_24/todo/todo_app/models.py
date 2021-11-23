from django.db import models


class TodoItem(models.Model):
    title = models.CharField(max_length=50, blank=False)
    content = models.TextField(blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_edit_day = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey('User',
                              on_delete=models.SET_NULL,
                              null=True,
                              related_name='todo_items')
    # NEW
    tags = models.ForeignKey('Tags',
                             on_delete=models.SET_NULL,
                             null=True,
                             related_name='tags')

    def __str__(self):
        return f'{self.owner}: {self.title}'

    class Meta:
        db_table = 'todo_item'


class User(models.Model):
    # default related name: TodoItem_set
    name = models.CharField(max_length=50, blank=False)
    telegram_id = models.BigIntegerField(blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}: {self.telegram_id}'


# NEW
class Tags(models.Model):
    name = models.TextField(blank=False)

    def __str__(self):
        return f'{self.name}'
