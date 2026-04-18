from django.urls import path
from .views import BookAppointmentView, DoctorAppointmentsView


urlpatterns = [

    path("book/", BookAppointmentView.as_view()),

    path("doctor-appointments/", DoctorAppointmentsView.as_view()),

]