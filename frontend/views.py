
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
        Receita.objects
        .filter(status='publicada')
        .select_related('categoria')
        .prefetch_related(
            'ingredientes_utilizados__ingrediente'
        ),
        slug=slug
    )

    context = {
        'receita': receita,
        'ingredientes': receita.ingredientes_utilizados.all(),
    }

    return render(request, 'frontend/receita.html', context)
