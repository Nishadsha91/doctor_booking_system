from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated

from .models import LeaveRequest
from .serializers import LeaveRequestSerializer, LeaveApprovalSerializer
from .permissions import IsDoctor, IsSuperAdmin


class CreateLeaveRequestView(CreateAPIView):

    serializer_class = LeaveRequestSerializer

    permission_classes = [IsAuthenticated, IsDoctor]

    def perform_create(self, serializer):

        doctor = self.request.user.doctor_profile

        serializer.save(doctor=doctor)

class MyLeaveRequestsView(ListAPIView):

    serializer_class = LeaveRequestSerializer

    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):

        doctor = self.request.user.doctor_profile

        return LeaveRequest.objects.filter(doctor=doctor)
    


class AllLeaveRequestsView(ListAPIView):

    queryset = LeaveRequest.objects.all()

    serializer_class = LeaveRequestSerializer

    permission_classes = [IsAuthenticated, IsSuperAdmin]


class LeaveApprovalView(UpdateAPIView):

    queryset = LeaveRequest.objects.all()

    serializer_class = LeaveApprovalSerializer

    permission_classes = [IsAuthenticated, IsSuperAdmin]