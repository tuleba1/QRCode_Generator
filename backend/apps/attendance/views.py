from django.db import IntegrityError

from django.shortcuts import render
from datetime import date
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status   


from students.models import Student
from .models import Attendance
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