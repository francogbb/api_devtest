from django.contrib.admin import register, ModelAdmin
from .models import Type_Player, Player, Team


# Register your models here.
@register(Type_Player)
class TypePlayerAdmin(ModelAdmin):
    list_display = ("type_name", "description")

@register(Player)
class PlayerAdmin(ModelAdmin):
    list_display = ("nickname", "age", "nationality", "type_player")

@register(Team)
class TeamAdmin(ModelAdmin):
    list_display = ("team_name", "country", "coach")