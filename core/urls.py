from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("mission/<int:mission_id>/", views.mission_detail, name="mission_detail"),
    path("hackers/", views.hackers, name="hackers"),
    path("corporations/", views.corporations, name="corporations"),
    path("corporation/<int:corp_id>/", views.corporation_detail, name="corporation_detail"),
    path("mission/<int:mission_id>/apply/", views.apply_mission, name="apply_mission"),
    path("hacker/<int:hacker_id>/", views.hacker_detail, name="hacker_detail"),
    path("implants/", views.implants, name="implants"),
    path("implant/<int:implant_id>/", views.implant_detail, name="implant_detail"),
    path("top/", views.top_hackers, name="top"),
    path("news/<int:post_id>/", views.news_detail, name="news_detail"),
    path("news", views.news_list, name="news_list"),
]