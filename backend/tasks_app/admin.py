from django.contrib import admin
from .models import Category, Task

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id','name','created_at')

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('id','title','user','created_at','due_date','notified')
    list_filter = ('notified',)
