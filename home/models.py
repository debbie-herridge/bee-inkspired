from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Tag model
class Tag(models.Model):
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

# Flash designs model
class Design(models.Model):
    name = models.CharField(max_length=200, null=True)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

# Appointment booking model
class Booking(models.Model):
    PREFERENCE = (
        ('radio','Radio'),
        ('talking','Talking'),
        ('silence','Silence'),
        ('not fused','Not fused')
    )
    date = models.DateField(default=date.today)
    customer = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    design = models.ForeignKey(Design, null=True, on_delete=models.SET_NULL)
    available = models.BooleanField(default=True)
    preference = models.CharField(max_length=200, null=True, choices=PREFERENCE)

# User upload image enquiry
class Enquiry(models.Model):
    customer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    enquiry = models.CharField(max_length=500, null=True)
    image = models.FileField(upload_to='customer-enqiries')