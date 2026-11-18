import nh3
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.db.models import Q, Count
from django.template.loader import render_to_string

from receitas.models import Receita
from categorias.models import Categoria
from ingredientes.models import Ingrediente


def home(request):
    categorias = Categoria.objects.all()
    ingredientes = Ingrediente.objects.all()

    return render(request, 'frontend/home.html', {
        'categorias': categorias,
        'ingredientes': ingredientes,
    })


def buscar_ingredientes(request):
    termo = request.GET.get('q', '').strip()

    ingredientes = []

    if len(termo) >= 2:
        ingredientes = list(
            Ingrediente.objects.filter(
                nome__icontains=termo
            ).order_by('nome').values('id', 'nome')[:10]
        )

    return JsonResponse({'ingredientes': ingredientes})


def buscar_receitas(request):
    termo = request.GET.get('q', '').strip()
    ingredientes_ids = request.GET.getlist('ingredientes')

    receitas = Receita.objects.filter(
        status='publicada'
    ).select_related('categoria')

    if termo:
        receitas = receitas.filter(
            Q(nome__icontains=termo) |
            Q(descricao__icontains=termo) |
            Q(categoria__nome__icontains=termo)
        )

    if ingredientes_ids:
        receitas = (
            receitas
            .filter(
                ingredientes_utilizados__ingrediente__id__in=ingredientes_ids
            )
            .annotate(
                total_ingredientes_selecionados=Count(
                    'ingredientes_utilizados__ingrediente',
                    filter=Q(
                        ingredientes_utilizados__ingrediente__id__in=ingredientes_ids
                    ),
                    distinct=True
                )
            )
            .filter(
                total_ingredientes_selecionados=len(set(ingredientes_ids))
            )
        )

    receitas = receitas.distinct().order_by('-data_criacao')

    return render(
        request,
        'frontend/partials/cards_receitas.html',
        {'receitas': receitas}
    )


def detalhe_receita(request, slug):
    receita = get_object_or_404(
        Receita.objects.filter(status='publicada')
        .select_related('categoria')
        .prefetch_related('ingredientes_utilizados__ingrediente'),
        slug=slug
    )

    modo_preparo_html = nh3.clean(
        receita.modo_preparo,
        tags={
            'p', 'br',
            'strong', 'b',
            'em', 'i',
            'u',
            'ul', 'ol', 'li',
            'h2', 'h3',
            'a',
        },
        attributes={
            'a': {'href', 'title'},
        },
        url_schemes={'http', 'https', 'mailto'},
    )

    return render(request, 'frontend/receita.html', {
        'receita': receita,
        'ingredientes': receita.ingredientes_utilizados.all(),
        'modo_preparo_html': modo_preparo_html,
    })