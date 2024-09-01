from django.contrib import admin
from .models import CustomUserModel

@admin.register(CustomUserModel)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'nick_name', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')



