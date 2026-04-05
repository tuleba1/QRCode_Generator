from django.urls import path
from .views import AttendanceScanView



urlpatterns = [    path('scan/', AttendanceScanView.as_view(), name='attendance-scan'),
]