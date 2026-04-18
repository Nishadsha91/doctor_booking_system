from django.db import models
from doctors.models import Doctor

class LeaveRequest(models.Model):

    STATUS = (
        ('pending','Pending'),
        ('approved','Approved'),
        ('rejected','Rejected')
    )

    doctor = models.ForeignKey(Doctor,on_delete=models.CASCADE)

    date = models.DateField()

    reason = models.TextField()

    status = models.CharField(max_length=20,choices=STATUS,default='pending')
    created_at = models.DateTimeField(auto_now_add=True)