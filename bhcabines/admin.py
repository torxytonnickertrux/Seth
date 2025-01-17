from django.contrib import admin
from .models import UserRequest

@admin.register(UserRequest)
class UserRequestAdmin(admin.ModelAdmin):
    list_display = ('client_ip', 'user_agent', 'created_at')
    search_fields = ('client_ip', 'user_agent')
