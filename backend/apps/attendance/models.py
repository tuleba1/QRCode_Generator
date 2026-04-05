from django.db import models
import uuid



class Attendance(models.Model):
    #Registro diário de presença do estudante, garantindo que cada estudante tenha apenas um registro por dia.

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    student = models.ForeignKey(
        "students.Student",
        on_delete=models.CASCADE,
        related_name="attendances",
        help_text="Estudante associado ao registro de presença"
    )

    date = models.DateField(help_text="Data da presença registrada")

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', 'created_at']
        verbose_name = "Presença"
        verbose_name_plural = "Presenças"
        constraints = [
            models.UniqueConstraint(
                fields=['student', 'date'],
                name='unique_attendance_per_day'
            )
        ]

        def __str__(self):
            return f"Presença de {self.student.name} em {self.date}"