from django import forms
from .models import Owner, Pet, Event


class OwnerForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ["first_name", "last_name", "phone_number", "city"]


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = [
            "pet_name",
            "pet_age",
            "photo",
            "species",
            "breed",
            "gender",
            "isFixed",
        ]
