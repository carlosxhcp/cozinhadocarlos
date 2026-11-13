from django.contrib import admin
from .models import Ingrediente


@admin.register(Ingrediente)
class IngredienteAdmin(admin.ModelAdmin):

    list_display = ('nome',)
    search_fields = ('nome',)
    ordering = ('nome',)