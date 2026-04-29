from django.shortcuts import render, get_object_or_404
from .models import Mission, Hacker, Corporation, Implant, NewsPost


def index(request):
    missions = Mission.objects.select_related("corporation").filter(status="open")
    news     = NewsPost.objects.all()[:5]
    return render(request, "core/index.html", {"missions": missions, "news": news})


def mission_detail(request, mission_id):
    mission = get_object_or_404(Mission, id=mission_id)
    return render(request, "core/mission_detail.html", {"mission": mission})


def hackers(request):
    hacker_list = Hacker.objects.select_related("corporation").all()
    return render(request, "core/hackers.html", {"hackers": hacker_list})


def corporations(request):
    corp_list = Corporation.objects.all().order_by("name")
    return render(request, "core/corporations.html", {"corporations": corp_list})


def corporation_detail(request, corp_id):
    corp = get_object_or_404(Corporation, id=corp_id)
    missions = corp.missions.all()
    hackers = corp.hackers.all()
    return render(request, "core/corporation_detail.html", {
        "corporation": corp,
        "missions": missions,
        "hackers": hackers,
    })