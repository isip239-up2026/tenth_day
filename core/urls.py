from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("mission/<int:mission_id>/", views.mission_detail, name="mission_detail"),
    path("hackers/", views.hackers, name="hackers"),
]
