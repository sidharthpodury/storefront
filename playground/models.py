from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Person(models.Model):
    email = models.CharField(max_length=100, null=True)
    fname = models.CharField(max_length=100, null=True)
    lname = models.CharField(max_length=100, null=True)
    valid_email = models.BooleanField(null=True)

    def __str__(self):
        return str(self.fname)

class Validation(models.Model):
    validation_code = models.IntegerField()
    person = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return str(self.pk)
    
class Invitation(models.Model):
    sender = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    
    def __str__(self):
        return str(self.pk)

class Timeslot(models.Model):
    invitee = models.ForeignKey(Person, on_delete=models.CASCADE, null=True)
    invitation = models.ForeignKey(Invitation, on_delete=models.CASCADE, null=True)
    selected_dt = models.TextField()

    def __str__(self):
        return str(self.selected_dt)
