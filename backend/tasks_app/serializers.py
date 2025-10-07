from rest_framework import serializers
from .models import Task, Category
from users.serializers import UserSerializer

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id','name','created_at')

class TaskSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    category_names = serializers.ListField(write_only=True, required=False, child=serializers.CharField())
    user = serializers.PrimaryKeyRelatedField(read_only=True)
    class Meta:
        model = Task
        fields = ('id','user','title','description','categories','category_names','created_at','due_date','notified')

    def create(self, validated_data):
        names = validated_data.pop('category_names', [])
        task = Task.objects.create(**validated_data)
        for n in names:
            cat, _ = Category.objects.get_or_create(name=n)
            task.categories.add(cat)
        return task
