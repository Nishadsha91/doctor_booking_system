from django.db import models
from django.conf import settings

User = settings.AUTH_USER_MODEL

class Doctor(models.Model):

    user = models.OneToOneField(
    User,
    on_delete=models.CASCADE,
    related_name="doctor_profile"
)

    working_days = models.JSONField()

    start_time = models.TimeField()

    end_time = models.TimeField()

    slot_duration = models.IntegerField()

    consultation_per_day = models.IntegerField()