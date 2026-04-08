from django.urls import path
from .views import checkin_page, confirm_attendance, generate_qr_page



urlpatterns = [    
        path("generate/", generate_qr_page),
        path("checkin/", checkin_page),
        path("confirm/", confirm_attendance),
             
]