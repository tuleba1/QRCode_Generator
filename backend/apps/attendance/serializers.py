from rest_framework import serializers


class AttendanceSerializer(serializers.Serializer):
    qr_token = serializers.UUIDField()
    