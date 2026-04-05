from django.contrib import admin
from .models import Attendance
# Register your models here.

@admin.register(Attendance)

# Administração personalizada para o modelo Attendance

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "date" , "created_at")
    list_filter = ("date",)
    search_fields = ("student__name", "student__registration")