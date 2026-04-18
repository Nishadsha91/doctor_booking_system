from rest_framework import serializers
from .models import LeaveRequest


class LeaveRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = LeaveRequest
        fields = [
            "id",
            "doctor",
            "date",
            "reason",
            "status",
            "created_at"
        ]
        read_only_fields = ["status", "created_at"]

class LeaveApprovalSerializer(serializers.ModelSerializer):

    class Meta:
        model = LeaveRequest
        fields = ["status"]