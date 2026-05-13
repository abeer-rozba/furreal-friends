from django.shortcuts import render, redirect, get_object_or_404
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
from .models import Owner, Pet, Event
from .forms import OwnerForm, PetForm, EventForm


# Create your views here.
def show_homepage(request):
    return render(request, "homepage.html")


@login_required
def check_profile(request):
    if hasattr(request.user, "owner"):
        return redirect("/")
    return redirect("/owners/new/")


@login_required
def toggle_follow(request, id):
    user_account = request.user.owner
    target_account = get_object_or_404(Owner, id=id)

    if user_account != target_account:
        if target_account in user_account.following.all():
            user_account.following.remove(target_account)
        else:
            user_account.following.add(target_account)
    return redirect(f"/community/{id}")


def toggle_register(request, id):
    event = get_object_or_404(Event, id=id)
    owner = request.user.owner

    if owner in event.attendees.all():
        event.attendees.remove(owner)
    else:
        event.attendees.add(owner)

    return redirect(f"/events/{id}")


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


class EventCreateView(CreateView):
    model = Event
    form_class = EventForm
    template_name = "pet-events/event-form.html"
    success_url = "/events/"

    def form_valid(self, form):
        form.instance.host = self.request.user.owner
        return super().form_valid(form)


class EventListView(ListView):
    model = Event
    template_name = "pet-events/all-events.html"
    context_object_name = "events"


class EventDetailView(DetailView):
    model = Event
    template_name = "pet-events/event-details.html"
    context_object_name = "event"
    pk_url_kwarg = "id"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            owner = self.request.user.owner
        else:
            owner = None

        event = self.get_object()

        followed_attendees = []

        if owner:
            followed_attendees = event.attendees.filter(id__in=owner.following.all())

        context["followed_attendees"] = followed_attendees
        return context


class MyEventsListView(ListView):
    model = Event
    template_name = "pet-events/my-events.html"
    context_object_name = "events"


class EventUpdateView(UpdateView):
    model = Event
    template_name = "pet-events/event-form.html"
    form_class = EventForm
    pk_url_kwarg = "id"

    def get_success_url(self):
        return f"/events/{self.object.id}"

    def form_valid(self, form):
        form.instance.host = self.request.user.owner
        return super().form_valid(form)


class EventDeleteView(DeleteView):
    model = Event
    success_url = "/events/my-events/"
    pk_url_kwarg = "id"
