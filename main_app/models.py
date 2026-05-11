from django.core.exceptions import ValidationError
import phonenumbers
from django.db import models
from django.contrib.auth.models import User
from phonenumber_field.modelfields import PhoneNumberField


def only_bh_numbers(value):
    if value:
        country = phonenumbers.region_code_for_number(value)
        if country != "BH":
            raise ValidationError("You must register with a Bahraini phone number!")


# Create your models here.
class Owner(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone_number = PhoneNumberField(region="BH", validators=[only_bh_numbers])
    city = models.CharField(max_length=50)

    def __str__(self):
        return self.first_name


class Pet(models.Model):
    pet_name = models.CharField(max_length=50)
    pet_age = models.IntegerField()
    photo = models.CharField()
    species = models.CharField(max_length=50)
    breed = models.CharField(max_length=50)
    gender = models.CharField(max_length=6)
    isFixed = models.BooleanField()
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, related_name="pets")
    friends = models.ManyToManyField("self", blank=True)


class Event(models.Model):
    host = models.ForeignKey(
        Owner, on_delete=models.CASCADE, related_name="hosted_event"
    )
    title = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    description = models.TextField()
    capacity = models.IntegerField()
    mustReserve = models.BooleanField()
    attendees = models.ManyToManyField("Owner", blank=True)
