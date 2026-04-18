from django.db import models
from doctors.models import Doctor
from accounts.models import User

class Appointment(models.Model):

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)

    customer = models.ForeignKey(User, on_delete=models.CASCADE)

    date = models.DateField()

    slot_time = models.TimeField()

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("doctor", "date", "slot_time")