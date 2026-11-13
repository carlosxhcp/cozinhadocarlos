import nh3
from django.shortcuts import render, get_object_or_404

from receitas.models import Receita
from categorias.models import Categoria


def home(request):
    receitas = (
        Receita.objects
        .filter(status='publicada')
        .select_related('categoria')
        .order_by('-data_criacao')[:8]
    )

    categorias = Categoria.objects.all()

    context = {
        'receitas': receitas,
        'categorias': categorias,
    }

    return render(request, 'frontend/home.html', context)


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