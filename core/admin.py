from django.contrib import admin
from .models import Corporation, Hacker, Mission, Implant, MissionApplication, NewsPost


@admin.register(Corporation)
class CorporationAdmin(admin.ModelAdmin):
    list_display  = ["name", "slogan", "founded"]
    search_fields = ["name"]


@admin.register(Hacker)
class HackerAdmin(admin.ModelAdmin):
    list_display  = ["handle", "rank", "rep", "corporation"]
    list_filter   = ["rank"]
    search_fields = ["handle"]


@admin.register(Mission)
class MissionAdmin(admin.ModelAdmin):
    list_display  = ["title", "difficulty", "reward", "status", "corporation"]
    list_filter   = ["status", "difficulty"]
    search_fields = ["title"]


@admin.register(Implant)
class ImplantAdmin(admin.ModelAdmin):
    list_display = ["name", "slot", "price", "manufacturer"]
    list_filter  = ["slot"]


@admin.register(MissionApplication)
class MissionApplicationAdmin(admin.ModelAdmin):
    list_display = ["hacker", "mission", "applied_at"]


@admin.register(NewsPost)
class NewsPostAdmin(admin.ModelAdmin):
    list_display = ["title", "source", "views", "posted_at"]
