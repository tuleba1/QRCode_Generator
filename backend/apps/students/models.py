from django.db import models
import uuid
import qrcode
from io import BytesIO
from django.core.files import File


class Student(models.Model):

    """
    Modelo do estudante.
    Cada aluno irá possuir um QR Token unitário, para registrar sua presença diária
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Identificador único do estudante

    name = models.CharField(max_length=255) # Aba para nome completo do estudante

    registration = models.CharField(max_length=20, unique=True, help_text= "Matrícula ou código do aluno")  # Aba de matrícula do estudante

    qr_token = models.UUIDField(default=uuid.uuid4, unique=True, help_text="Token único para registro de presença via QR Code")  # Token único para QR Code

    total_presences = models.PositiveIntegerField(default=0, help_text="Total de presenças registradas pelo estudante")  # Contador de presenças

    created_at = models.DateTimeField(auto_now_add=True)  # Data de criação do registro

    update_at = models.DateTimeField(auto_now=True)  # Data da última atualização do registro

    qr_code = models.ImageField(upload_to="qrcodes/", blank=True, null=True)

    class Meta:
        ordering = ['name']  # Ordenação padrão por nome do estudante
        verbose_name = "Estudante"
        verbose_name_plural = "Estudantes"

    def __str__(self):
        return f"{self.name} ({self.registration})" #Aba para nome completo do estudante e matrícula
    
    def save(self, *args, **kwargs):
        creating= self._state.adding  # Verifica se o registro está sendo criado pela primeira vez

        super().save(*args, **kwargs)  # Salva o registro para garantir que o ID e o QR token sejam gerados

        if creating and not self.qr_code:
            qr_data = qr_data = f"http://127.0.0.1:8000/attendance/checkin/?token={self.qr_token}"  #

            qr = qrcode.make(qr_data)

            buffer = BytesIO()
            qr.save(buffer, format="PNG")

            file_name = f"{self.registration}.png"

            self.qr_code.save(file_name, File(buffer), save=False)

            super().save(update_fields=["qr_code"])  # Salva apenas o campo do QR code para evitar loop infinito

