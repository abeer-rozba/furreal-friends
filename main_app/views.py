from django.shortcuts import render, redirect
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    UpdateView,
    DeleteView,
)
from django.http import HttpResponseRedirect
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Owner, Pet
from .forms import OwnerForm, PetForm


# Create your views here.
def show_homepage(request):
    return render(request, "homepage.html")


@login_required
def check_profile(request):
    if hasattr(request.user, "owner"):
        return redirect("/")
    return redirect("/owners/new/")


class SignUpView(CreateView):
    template_name = "registration/signup.html"
    form_class = UserCreationForm
    success_url = "/auth/login"


class OwnerCreateView(CreateView):
    model = Owner
    form_class = OwnerForm
    success_url = "/"
    template_name = "owners/owner-form.html"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class OwnerDetailView(DetailView):
    model = Owner
    template_name = "owners/owner-details.html"
    context_object_name = "owner"
    pk_url_kwarg = "id"


class OwnerUpdateView(UpdateView):
    model = Owner
    template_name = "owners/owner-form.html"
    form_class = OwnerForm
    pk_url_kwarg = "id"

    def get_success_url(self):
        return f"/owners/{self.object.id}"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class OwnerDeleteView(DeleteView):
    model = Owner
    pk_url_kwarg = "id"
    success_url = "/signup/"

    def get_queryset(self):
        return Owner.objects.filter(user=self.request.user)

    def form_valid(self, form):
        user = self.object.user
        logout(self.request)
        user.delete()
        return HttpResponseRedirect(self.success_url)


class CommunityListView(ListView):
    model = Owner
    template_name = "community/all-members.html"
    context_object_name = "members"


class CommunityDetailView(DetailView):
    model = Owner
    template_name = "community/member-details.html"
    context_object_name = "member"
    pk_url_kwarg = "id"


class PetCreateView(CreateView):
    model = Pet
    form_class = PetForm
    template_name = "pets/pet-form.html"

    def get_success_url(self):
        return f"/pets/{self.object.id}"

    def form_valid(self, form):
        form.instance.owner = self.request.user.owner
        return super().form_valid(form)


class PetDetailView(DetailView):
    model = Pet
    template_name = "pets/pet-details.html"
    context_object_name = "pet"
    pk_url_kwarg = "id"


class PetListView(ListView):
    model = Pet
    template_name = "pets/all-pets.html"
    context_object_name = "pets"


class MyPetsListView(ListView):
    model = Pet
    template_name = "pets/my-pets.html"
    context_object_name = "pets"


class MemberPetsDetailView(DetailView):
    model = Owner
    template_name = "pets/member-pets.html"
    context_object_name = "member"
    pk_url_kwarg = "id"


class PetUpdateView(UpdateView):
    model = Pet
    template_name = "pets/pet-form.html"
    form_class = PetForm
    pk_url_kwarg = "id"

    def get_success_url(self):
        return f"/pets/{self.object.id}"

    def form_valid(self, form):
        form.instance.owner = self.request.user.owner
        return super().form_valid(form)


class PetDeleteView(DeleteView):
    model = Pet
    success_url = "/my-pets/"
    pk_url_kwarg = "id"
