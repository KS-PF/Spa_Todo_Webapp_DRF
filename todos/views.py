from .models import TodoModel
from todos.serializers import TodoSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404


class TodoListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        title = request.query_params.get('title', None)
        is_complete = request.query_params.get('is_complete', None)
        priority_status = request.query_params.get('priority_status', None)

        queryset = TodoModel.objects.filter(created_by=request.user).order_by('-created_at')

        if is_complete is not [True, False]:
            is_complete = None

        PRIORITY_CHOICES = ['低い', '普通', '高い', '緊急',]
        if priority_status not in PRIORITY_CHOICES:
            priority_status = None

        if title:
            queryset = queryset.filter(title__contains=title)
        if is_complete:
            queryset = queryset.filter(is_complete=is_complete)
        if priority_status:
            queryset = queryset.filter(priority_status=priority_status)

        serializer = TodoSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = TodoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(created_by=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TodoDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_object(self, pk, user):
        try:
            return TodoModel.objects.get(created_by=user, pk=pk)
        except TodoModel.DoesNotExist:
            raise Http404

    def get(self, request, pk, *args, **kwargs):
        todo = self.get_object(pk, request.user)
        serializer = TodoSerializer(todo)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, pk, *args, **kwargs):
        todo = self.get_object(pk, request.user)
        serializer = TodoSerializer(todo, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, *args, **kwargs):
        todo = self.get_object(pk, request.user)
        todo.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)