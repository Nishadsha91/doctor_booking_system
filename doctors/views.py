from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render

from .models import Doctor
from accounts.models import User
from .serializers import DoctorSerializer
from .utils import generate_slots
from django.contrib.auth.decorators import login_required
from appointments.models import Appointment
from leave.models import LeaveRequest


class DoctorListView(ListAPIView):

    queryset = Doctor.objects.all()

    serializer_class = DoctorSerializer




class DoctorSlotsView(APIView):

    def get(self, request, doctor_id):

        date = request.query_params.get("date")

        if not date:
            return Response({"error": "date required"}, status=400)

        doctor = get_object_or_404(Doctor, id=doctor_id)

        date_obj = datetime.strptime(date, "%Y-%m-%d").date()

        weekday = date_obj.strftime("%a").lower()

        if weekday not in doctor.working_days:
            return Response({"slots": []})

        # check leave first
        leave = LeaveRequest.objects.filter(
            doctor=doctor,
            date=date_obj,
            status="approved"
        ).exists()

        if leave:
            return Response({"slots": []})

        # generate slots
        slots = generate_slots(
            doctor.start_time,
            doctor.end_time,
            doctor.slot_duration
        )

        # remove booked slots
        booked = Appointment.objects.filter(
            doctor=doctor,
            date=date_obj
        ).values_list("slot_time", flat=True)

        available_slots = [s for s in slots if s not in booked]

        return Response({"slots": available_slots})
    



@login_required
def doctor_list_dashboard(request):

    doctors = Doctor.objects.all()

    return render(request, "dashboard/doctor_list.html", {"doctors": doctors})


@login_required
def create_doctor(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")
        slot_duration = request.POST.get("slot_duration")

        user = User.objects.create_user(
            username=username,
            password=password,
            role="doctor"
        )

        Doctor.objects.create(
            user=user,
            working_days=["mon","tue","wed","thu","fri"],
            start_time=start_time,
            end_time=end_time,
            slot_duration=slot_duration,
            consultation_per_day=20
        )

        return redirect("doctor-list-dashboard")

    return render(request, "dashboard/doctor_create.html")


@login_required
def delete_doctor(request, doctor_id):

    doctor = get_object_or_404(Doctor, id=doctor_id)

    doctor.delete()

    return redirect("doctor-list-dashboard")