from django.contrib import admin
from .models import Attendace
# Register your models here.

@admin.register(Attendace)

# Administração personalizada para o modelo Attendance

class AttendanceAdmin(admin.ModelAdmin):
    list_display = ("student", "date" , "created_at")
    list_filter = ("date",)
    search_fields = ("student__name", "student__registration")