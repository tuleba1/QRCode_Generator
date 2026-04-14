import base64
import qrcode

from io import BytesIO
from django.db import IntegrityError
from django.shortcuts import render
from datetime import date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status   
from students.models import Student
from .models import Attendance, QRSession
from .serializers import AttendanceSerializer





class AttendanceScanView(APIView):
    #View para processar a leitura do QR code e registrar a presença do estudante.
    def post(self, request):
        serializer = AttendanceSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        qr_token = serializer.validated_data["qr_token"]

        #Tentar buscar aluno

        try:
            student = Student.objects.get(qr_token=qr_token)
        except Student.DoesNotExist:
            return Response(
                    {"error": "QR code inválido ou estudante não encontrado."},
                    status=status.HTTP_404_NOT_FOUND
                )
        today = date.today()

        #Tentar criar o registro de presença   

        try:
            Attendance.objects.create(student=student, date=today)

            student.total_presences += 1
            student.save()

            return Response(
                {"status": "Presençar registrada com sucesso.",
                 "student": student.name,
                 "date": today,
                 "total_presences": student.total_presences},
                status=status.HTTP_201_CREATED
            )
        
        except IntegrityError:
            return Response(
                {"error": "Presença já registrada para este estudante hoje."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
def checkin_page(request):
    token = request.GET.get("session")

    session = None

    if token:
        try:
            session = QRSession.objects.get(token=token)
        except QRSession.DoesNotExist:
            session = None

    if not session or not session.is_valid():
        return render(request, "attendance/expired.html")

    return render(request, "attendance/checkin.html", {
        "session_token": token
    })
        
def confirm_attendance(request):
    if request.method == "POST":
        name = request.POST.get("name")
        token = request.POST.get("session")

        try:
            session = QRSession.objects.get(token=token)
        except QRSession.DoesNotExist:
            return render(request, "attendance/expired.html")

        if not session.is_valid():
            return render(request, "attendance/expired.html")

        student = Student.objects.filter(name=name).first()

        if not student:
            return render(request, "attendance/error.html", {"msg": "Aluno não encontrado"})

        today = date.today()

        try:
            Attendance.objects.create(student=student, date=today)

            student.total_presences += 1
            student.save()

            return render(request, "attendance/success.html", {"student": student})

        except IntegrityError:
            return render(request, "attendance/already.html", {"student": student})
        
import base64

def generate_qr_page(request):

    session = QRSession.objects.create()


    qr_data = request.build_absolute_uri(
        f"/attendance/checkin/?session={session.token}"
    )


    qr = qrcode.QRCode(
        version=1,
        box_size=12,
        border=5
    )

    qr.add_data(qr_data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")


    buffer = BytesIO()
    img.save(buffer, format="PNG")

    qr_base64 = base64.b64encode(buffer.getvalue()).decode()


    return render(request, "attendance/generate_qr.html", {
        "qr_image": qr_base64,
        "qr_url": qr_data  # 👈 útil pra debug
    })
    