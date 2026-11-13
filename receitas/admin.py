from django.contrib import admin
from .models import Receita, ReceitaIngrediente


class ReceitaIngredienteInline(admin.TabularInline):
    model = ReceitaIngrediente
    extra = 1


@admin.register(Receita)
class ReceitaAdmin(admin.ModelAdmin):
    list_display = (
        'nome',
        'categoria',
        'tempo_preparo',
        'rendimento',
        'data_criacao',
    )

    list_filter = ('categoria', 'data_criacao')
    search_fields = ('nome', 'descricao')
    prepopulated_fields = {'slug': ('nome',)}
    inlines = [ReceitaIngredienteInline]
    ordering = ('-data_criacao',)