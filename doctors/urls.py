from django.urls import path
from .views import DoctorListView, DoctorSlotsView, doctor_list_dashboard, create_doctor, delete_doctor

urlpatterns = [

    path("list/", DoctorListView.as_view()),

    path("<int:doctor_id>/slots/", DoctorSlotsView.as_view()),

    path("dashboard/doctors/", doctor_list_dashboard, name="doctor-list-dashboard"),

    path("dashboard/doctors/create/", create_doctor, name="create-doctor"),

    path("dashboard/doctors/delete/<int:doctor_id>/", delete_doctor, name="delete-doctor"),

]



