from rest_framework import serializers
from .models import Doctor


class DoctorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Doctor
        fields = [
            "id",
            "user",
            "working_days",
            "start_time",
            "end_time",
            "slot_duration",
            "consultation_per_day"
        ]