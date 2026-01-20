from django.contrib import admin
from .models import Student 
# Register your models here.

@admin.register(Student)

# Administraçõa personalizada para o modelo Student

class StudentAdmin(admin.ModelAdmin):
    list_display = ("name", "registration", "total_presences", "created_at", "update_at")

    search_fields = ("name", "registration")