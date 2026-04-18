from rest_framework import serializers
from .models import Appointment


class AppointmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Appointment
        fields = [
            "id",
            "doctor",
            "customer",
            "date",
            "slot_time",
            "created_at"
        ]
        read_only_fields = ["customer", "created_at"]