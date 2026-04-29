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


def implants(request):
    slot = request.GET.get("slot")
    implant_list = Implant.objects.select_related("manufacturer").all()
    if slot:
        implant_list = implant_list.filter(slot=slot)
    return render(request, "core/implants.html", {"implants": implant_list})


def implant_detail(request, implant_id):
    implant = get_object_or_404(Implant, id=implant_id)
    return render(request, "core/implant_detail.html", {"implant": implant})