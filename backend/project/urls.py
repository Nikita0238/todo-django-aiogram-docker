from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from tasks_app import views as task_views

router = routers.DefaultRouter()
router.register(r'categories', task_views.CategoryViewSet, basename='category')
router.register(r'tasks', task_views.TaskViewSet, basename='task')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/telegram/<int:telegram_id>/tasks/', task_views.TelegramTasksView.as_view(), name='telegram_tasks'),
]
