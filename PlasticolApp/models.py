from email.policy import default
from pyexpat import model
from turtle import mode
from unittest.util import _MAX_LENGTH
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class Login(AbstractUser):
    userType = models.CharField(max_length=100)
    viewPass = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.username


class Civilians(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.IntegerField()
    address = models.CharField(max_length=300)
    ward = models.CharField(max_length=300, null=True)
    houseno = models.CharField(max_length=300, null=True)
    image = models.FileField(null=True)
    time=models.CharField(max_length=100,null=True)
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Staff(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone = models.IntegerField()
    age = models.IntegerField()
    ward = models.IntegerField()
    address = models.CharField(max_length=300)
    image = models.FileField(null=True)
    loginid = models.ForeignKey(Login, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Suggestions(models.Model):
    subject = models.CharField(max_length=100)
    details = models.CharField(max_length=300)
    date = models.DateField(auto_now=True)


class Waste(models.Model):
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE)
    civil_id = models.ForeignKey(Civilians, on_delete=models.CASCADE)
    weight = models.IntegerField()
    note = models.CharField(max_length=300)
    date = models.DateField(auto_now=True)
    status = models.CharField(max_length=100, default="Collected")


class Storage(models.Model):
    capacity = models.IntegerField(default=500)


class Complaints(models.Model):
    civilId = models.ForeignKey(Civilians, on_delete=models.CASCADE)
    desc = models.CharField(max_length=100)
    address = models.TextField()
    image = models.FileField()
    date = models.DateField(auto_now=True, null=True)
    status = models.CharField(max_length=100, default="Filed")

class Waste_request(models.Model):
    civil_id = models.ForeignKey(
        Civilians, on_delete=models.CASCADE, null=True, blank=True
    )
    staff_id = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True)
    weight = models.IntegerField(null=True, blank=True)
    desc = models.CharField(max_length=300)
    date = models.DateField(auto_now=True)
    status = models.CharField(max_length=100, default="Requested")
