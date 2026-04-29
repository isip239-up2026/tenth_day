from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Mission, Hacker, Corporation, Implant, NewsPost, MissionApplication
from .forms import ApplicationForm


def index(request):
    difficulty = request.GET.get("difficulty")
    status = request.GET.get("status")

    missions = Mission.objects.select_related("corporation").all()

    if difficulty:
        missions = missions.filter(difficulty=difficulty)
    if status:
        missions = missions.filter(status=status)

    paginator = Paginator(missions, 5)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    news = NewsPost.objects.all()[:5]


    filter_params = ""
    if difficulty:
        filter_params += f"&difficulty={difficulty}"
    if status:
        filter_params += f"&status={status}"

    return render(request, "core/index.html", {
        "missions": page_obj,
        "news": news,
        "filter_params": filter_params,
    })


def mission_detail(request, mission_id):
    from django.db.models import Q
    mission = get_object_or_404(Mission, id=mission_id)
    form = ApplicationForm()
    app_count = mission.applications.count()
    related = Mission.objects.filter(
        Q(difficulty=mission.difficulty) | Q(corporation=mission.corporation)
    ).exclude(id=mission.id)[:4]
    return render(request, "core/mission_detail.html", {
        "mission": mission,
        "form": form,
        "app_count": app_count,
        "related": related,
    })


def hackers(request):
    rank = request.GET.get("rank")
    sort = request.GET.get("sort", "-rep")
    hacker_list = Hacker.objects.select_related("corporation").all()

    if rank:
        hacker_list = hacker_list.filter(rank=rank)

    hacker_list = hacker_list.order_by(sort)

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


def hacker_detail(request, hacker_id):
    hacker = get_object_or_404(Hacker, id=hacker_id)
    applications = hacker.applications.select_related("mission").all()
    return render(request, "core/hacker_detail.html", {
        "hacker": hacker,
        "applications": applications,
    })


def implants(request):
    slot = request.GET.get("slot")
    implant_list = Implant.objects.select_related("manufacturer").all()
    if slot:
        implant_list = implant_list.filter(slot=slot)
    return render(request, "core/implants.html", {"implants": implant_list})


def implant_detail(request, implant_id):
    implant = get_object_or_404(Implant, id=implant_id)
    return render(request, "core/implant_detail.html", {"implant": implant})