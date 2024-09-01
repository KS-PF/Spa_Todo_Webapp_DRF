from django.contrib import admin
from .models import TodoModel

@admin.register(TodoModel)
class TodoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'is_complete', 'priority_status', 'created_by', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')