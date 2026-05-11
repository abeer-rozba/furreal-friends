from django.urls import path
from . import views

urlpatterns = [
    path("", views.show_homepage),
    path("signup/", views.SignUpView.as_view()),
    path("check-profile/", views.check_profile),
    path("owners/new/", views.OwnerCreateView.as_view()),
    path("owners/<int:id>", views.OwnerDetailView.as_view()),
    path("owners/<int:id>/update", views.OwnerUpdateView.as_view()),
    path("owners/<int:id>/delete", views.OwnerDeleteView.as_view()),
    path("community/", views.CommunityListView.as_view()),
    path("community/<int:id>", views.CommunityDetailView.as_view()),
    path("community/<int:id>/pets", views.MemberPetsDetailView.as_view()),
    path("my-pets/", views.MyPetsListView.as_view()),
    path("pets/", views.PetListView.as_view()),
    path("pets/new/", views.PetCreateView.as_view()),
    path("pets/<int:id>", views.PetDetailView.as_view()),
    path("pets/<int:id>/update/", views.PetUpdateView.as_view()),
    path("pets/<int:id>/delete", views.PetDeleteView.as_view()),
    path("events/new", views.EventCreateView.as_view()),
    path("events/", views.EventListView.as_view()),
]
