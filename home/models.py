from datetime import date
from django.db import models
from django.contrib.auth.models import User


class Tag(models.Model):
    """
    Simple tag model to catagorise designs.
    """
    name = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.name

class Design(models.Model):
    """
    Model for flash designs.
    """
    name = models.CharField(max_length=200, null=True)
    tags = models.ManyToManyField(Tag)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    """
    Model for customer review comment and scores.
    """
    RECOMMEND = (
        ('will not recommend','Will not recommend'),
        ('might recommend','Might recommend'),
        ('absolutely recommend','Absolutely recommend!'),
    )
    RATING = (
        ('1','1'),
        ('2','2'),
        ('3','3'),
        ('4','4'),
        ('5','5'),
    )
    customer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    rating = models.CharField(max_length=200, null=True, choices=RATING)
    recommend = models.CharField(max_length=200, null=True, choices=RECOMMEND)
    review = models.CharField(max_length=500, null=True)

class Booking(models.Model):
    """
    Booking appointment with relationship to all other models.
    """
    PREFERENCE = (
        ('radio','Radio'),
        ('talking','Talking'),
        ('silence','Silence'),
        ('not fused','Not fused')
    )
    date = models.DateField(default=date.today)
    customer = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    design = models.ForeignKey(Design, null=True, on_delete=models.SET_NULL)
    preference = models.CharField(max_length=200, null=True, choices=PREFERENCE)
    review = models.ForeignKey(Review, null=True, blank=True, on_delete=models.SET_NULL)

class Enquiry(models.Model):
    """
    Stores user enquiry and reference image.
    """
    customer = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    enquiry = models.CharField(max_length=500, null=True)
    image = models.FileField(upload_to='customer-enqiries')
