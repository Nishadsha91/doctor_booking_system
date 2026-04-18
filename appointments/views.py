from rest_framework.views import APIView 
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from django.shortcuts import get_object_or_404

from .models import Appointment
from .serializers import AppointmentSerializer
from .permissions import IsCustomer, IsDoctor

from doctors.models import Doctor
from doctors.utils import generate_slots

from leave.models import LeaveRequest
from datetime import datetime


class BookAppointmentView(APIView):

    permission_classes = [IsAuthenticated, IsCustomer]

    @transaction.atomic
    def post(self, request):

        doctor_id = request.data.get("doctor")

        date = request.data.get("date")

        slot_time = request.data.get("slot_time")

        doctor = get_object_or_404(Doctor, id=doctor_id)

        weekday = datetime.strptime(date, "%Y-%m-%d").strftime("%a").lower()

        if weekday not in doctor.working_days:
            return Response({"error": "Doctor not working this day"})

        # check leave
        leave = LeaveRequest.objects.filter(
            doctor=doctor,
            date=date,
            status="approved"
        ).exists()

        if leave:
            return Response({"error": "Doctor on leave"})

        # generate slots
        slots = generate_slots(
            doctor.start_time,
            doctor.end_time,
            doctor.slot_duration
        )

        slot_time_obj = None
        for fmt in ("%H:%M:%S", "%H:%M"):
            try:
                slot_time_obj = datetime.strptime(slot_time, fmt).time()
                break
            except (ValueError, TypeError):
                continue

        if slot_time_obj is None or slot_time_obj not in slots:
            return Response({"error": "Invalid slot"})

        # check double booking
        if Appointment.objects.filter(
            doctor=doctor,
            date=date,
            slot_time=slot_time_obj
        ).exists():

            return Response({"error": "Slot already booked"})

        appointment = Appointment.objects.create(
            doctor=doctor,
            customer=request.user,
            date=date,
            slot_time=slot_time_obj
        )

        serializer = AppointmentSerializer(appointment)

        return Response(serializer.data)
    



class DoctorAppointmentsView(ListAPIView):

    serializer_class = AppointmentSerializer

    permission_classes = [IsAuthenticated, IsDoctor]

    def get_queryset(self):

        doctor = self.request.user.doctor_profile

        return Appointment.objects.filter(doctor=doctor)