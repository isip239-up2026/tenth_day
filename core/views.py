from django.shortcuts import render, get_object_or_404, redirect
from .models import Mission, Hacker, Corporation, Implant, NewsPost, MissionApplication
from .forms import ApplicationForm


def index(request):
    missions = Mission.objects.select_related("corporation").filter(status="open")
    news     = NewsPost.objects.all()[:5]
    return render(request, "core/index.html", {"missions": missions, "news": news})


def mission_detail(request, mission_id):
    mission = get_object_or_404(Mission, id=mission_id)
    form = ApplicationForm()
    app_count = mission.applications.count()
    return render(request, "core/mission_detail.html", {
        "mission": mission,
        "form": form,
        "app_count": app_count,
    })


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


def apply_mission(request, mission_id):
    mission = get_object_or_404(Mission, id=mission_id)
    form = ApplicationForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        handle = form.cleaned_data["hacker_handle"]
        hacker = Hacker.objects.filter(handle__iexact=handle).first()

        if not hacker:
            form.add_error("hacker_handle", "Хакер с таким псевдонимом не найден.")
        elif MissionApplication.objects.filter(mission=mission, hacker=hacker).exists():
            form.add_error("hacker_handle", "Вы уже подавали заявку на эту миссию.")
        else:
            MissionApplication.objects.create(
                mission=mission,
                hacker=hacker,
                message=form.cleaned_data["message"]
            )
            return redirect("mission_detail", mission_id=mission.id)

    return render(request, "core/mission_detail.html", {
        "mission": mission,
        "form": form,
        "app_count": mission.applications.count(),
    })