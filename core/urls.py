from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("mission/<int:mission_id>/", views.mission_detail, name="mission_detail"),
    path("hackers/", views.hackers, name="hackers"),
    path("corporations/", views.corporations, name="corporations"),
    path("corporation/<int:corp_id>/", views.corporation_detail, name="corporation_detail"),
]
