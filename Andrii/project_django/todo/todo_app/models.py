from django.db import models


class TodoItem(models.Model):
    title = models.CharField(max_length=50, blank=False)
    content = models.TextField(blank=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    last_edit_date = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey("User", on_delete=models.SET_NULL,
                              null=True,
                              related_name="todo_items")
    tags = models.ForeignKey("Tags", default="general",
                             on_delete=models.SET_DEFAULT, null=True,
                             related_name="items")

    def __str__(self):
        return f'{self.owner}:{self.title}'

    class Meta:
        db_table = "todo_item"


class User(models.Model):
    name = models.CharField(max_length=50, blank=False)
    telegram_id = models.BigIntegerField(blank=False)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name}:{self.telegram_id}'


class Tags(models.Model):
    title = models.CharField(max_length=50, blank=False)

    def __str__(self):
        return f'{self.title}'


