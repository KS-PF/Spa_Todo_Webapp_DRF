from rest_framework import serializers
from todos.models import TodoModel


class TodoSerializer(serializers.ModelSerializer):
    id = serializers.CharField(read_only=True)
    class Meta:
        model = TodoModel
        fields = [
            'id',
            'title', 
            'is_complete', 
            'priority_status',
        ]
