import os
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Task, Category
from .serializers import TaskSerializer, CategorySerializer
from users.models import User
from django.shortcuts import get_object_or_404

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('-created_at')
    serializer_class = CategorySerializer
    permission_classes = [permissions.AllowAny]

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.context.get('user')
        if user:
            serializer.save(user=user)
        else:
            serializer.save()

class TelegramTasksView(APIView):
    permission_classes = []
    def get(self, request, telegram_id):
        secret = request.headers.get('X-BOT-SECRET')
        if secret != os.getenv('BOT_SHARED_SECRET'):
            return Response({'detail':'Forbidden'}, status=403)
        user = get_object_or_404(User, telegram_id=telegram_id)
        tasks = Task.objects.filter(user=user).order_by('-created_at')
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    def post(self, request, telegram_id):
        secret = request.headers.get('X-BOT-SECRET')
        if secret != os.getenv('BOT_SHARED_SECRET'):
            return Response({'detail':'Forbidden'}, status=403)
        user = get_object_or_404(User, telegram_id=telegram_id)
        data = request.data.copy()
        data['user'] = user.id
        serializer = TaskSerializer(data=data, context={'user': user})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)
