from django.db import models

# Create your models here.
class Person(models.Model):
    email = models.CharField(max_length=100)
    fname = models.CharField(max_length=100)
    lname = models.CharField(max_length=100)
    valid_email = models.BooleanField(null=True)

    def __str__(self):
        return self.fname

class Validation(models.Model):
    validation_code = models.IntegerField()
    person = models.ForeignKey(Person, on_delete=models.CASCADE)

