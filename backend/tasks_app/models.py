from django.db import models
from django.conf import settings
from ..snowflake import get_snowflake_id

class Category(models.Model):
    id = models.BigIntegerField(primary_key=True, default=get_snowflake_id)
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.name

class Task(models.Model):
    id = models.BigIntegerField(primary_key=True, default=get_snowflake_id)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    categories = models.ManyToManyField(Category, blank=True, related_name='tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(null=True, blank=True)
    notified = models.BooleanField(default=False)
    def __str__(self):
        return self.title
