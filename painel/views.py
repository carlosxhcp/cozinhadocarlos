from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from django.utils.text import slugify
from django.db.models import Q, ProtectedError
from django.contrib import messages

from receitas.models import Receita
from categorias.models import Categoria
from ingredientes.models import Ingrediente

from .forms import (
    ReceitaForm,
    ReceitaIngredienteFormSet,
    CategoriaForm,
    IngredienteForm,
)


# Permite acesso somente a usuários administradores.
admin_required = user_passes_test(
    lambda user: user.is_authenticated and user.is_staff,
    login_url='painel:login'
)


@admin_required
def dashboard(request):
    contexto = {
        'total_receitas': Receita.objects.count(),
        'total_categorias': Categoria.objects.count(),
        'total_ingredientes': Ingrediente.objects.count(),

        'receitas_recentes': Receita.objects.select_related(
            'categoria'
        ).order_by('-data_criacao')[:5],
    }

    return render(request, 'painel/dashboard.html', contexto)


@admin_required
def lista_receitas(request):
    busca = request.GET.get('q', '')

    receitas = Receita.objects.select_related('categoria').all()

    if busca:
        receitas = receitas.filter(
            Q(nome__icontains=busca) |
            Q(categoria__nome__icontains=busca)
        )

    contexto = {
        'receitas': receitas,
        'busca': busca,
    }

    return render(request, 'painel/receitas/lista.html', contexto)



@admin_required
def lista_rascunhos(request):
    busca = request.GET.get('q', '')

    receitas = Receita.objects.filter(
        status='rascunho'
    ).select_related('categoria')

    if busca:
        receitas = receitas.filter(
            Q(nome__icontains=busca) |
            Q(categoria__nome__icontains=busca)
        )

    return render(request, 'painel/receitas/rascunhos.html', {
        'receitas': receitas,
        'busca': busca,
    })



@admin_required
def criar_receita(request):
    receita = Receita()

    if request.method == 'POST':
        form = ReceitaForm(request.POST, request.FILES)
        formset = ReceitaIngredienteFormSet(request.POST, instance=receita)

        form_valido = form.is_valid()
        formset_valido = formset.is_valid()

        print("FORMULÁRIO VÁLIDO:", form_valido)
        print("ERROS DO FORMULÁRIO:", form.errors)
        print("FORMSET VÁLIDO:", formset_valido)
        print("ERROS DOS INGREDIENTES:", formset.errors)
        print("ERROS GERAIS DO FORMSET:", formset.non_form_errors())

        if form_valido and formset_valido:
            receita = form.save(commit=False)

            # Define o status conforme o botão pressionado
            status = request.POST.get('status', 'rascunho')

            if status not in ['rascunho', 'publicada']:
                status = 'rascunho'

            receita.status = status
            receita.save()

            formset.instance = receita
            formset.save()

            messages.success(request, 'Receita salva com sucesso!')
            return redirect('painel:lista_receitas')

    else:
        form = ReceitaForm()
        formset = ReceitaIngredienteFormSet(instance=receita)

    return render(request, 'painel/receitas/formulario.html', {
        'form': form,
        'formset': formset,
        'receita': receita,
    })

@admin_required
def editar_receita(request, pk):
    receita = get_object_or_404(Receita, pk=pk)

    if request.method == 'POST':
        form = ReceitaForm(request.POST, request.FILES, instance=receita)
        formset = ReceitaIngredienteFormSet(
            request.POST,
            instance=receita
        )

        if form.is_valid() and formset.is_valid():
            receita = form.save(commit=False)

            # Define o status conforme o botão pressionado
            status = request.POST.get('status', receita.status)

            if status not in ['rascunho', 'publicada']:
                status = receita.status

            receita.status = status
            receita.save()

            formset.instance = receita
            formset.save()

            messages.success(request, 'Receita atualizada com sucesso!')
            return redirect('painel:lista_receitas')

    else:
        form = ReceitaForm(instance=receita)
        formset = ReceitaIngredienteFormSet(instance=receita)

    return render(request, 'painel/receitas/formulario.html', {
        'form': form,
        'formset': formset,
        'receita': receita,
    })




@admin_required
def excluir_receita(request, pk):

    receita = get_object_or_404(Receita, pk=pk)

    if request.method == 'POST':
        receita.delete()
        return redirect('painel:lista_receitas')

    return render(request, 'painel/receitas/excluir.html', {
        'receita': receita,
    })


@admin_required
def lista_categorias(request):
    categorias = Categoria.objects.all()

    return render(request, 'painel/categorias/lista.html', {
        'categorias': categorias,
    })


@admin_required
def criar_categoria(request):
    if request.method == 'POST':
        form = CategoriaForm(request.POST, request.FILES)

        if form.is_valid():
            categoria = form.save(commit=False)

            if not categoria.slug:
                categoria.slug = slugify(categoria.nome)

            categoria.save()

            messages.success(request, 'Categoria cadastrada com sucesso!')
            return redirect('painel:lista_categorias')

    else:
        form = CategoriaForm()

    return render(request, 'painel/categorias/formulario.html', {
        'form': form,
        'titulo': 'Nova categoria',
    })


@admin_required
def editar_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == 'POST':
        form = CategoriaForm(
            request.POST,
            request.FILES,
            instance=categoria
        )

        if form.is_valid():
            categoria = form.save(commit=False)

            if not categoria.slug:
                categoria.slug = slugify(categoria.nome)

            categoria.save()

            messages.success(request, 'Categoria atualizada com sucesso!')
            return redirect('painel:lista_categorias')

    else:
        form = CategoriaForm(instance=categoria)

    return render(request, 'painel/categorias/formulario.html', {
        'form': form,
        'titulo': 'Editar categoria',
        'categoria': categoria,
    })


@admin_required
def excluir_categoria(request, pk):
    categoria = get_object_or_404(Categoria, pk=pk)

    if request.method == 'POST':
        try:
            categoria.delete()
            messages.success(request, 'Categoria excluída com sucesso!')

        except ProtectedError:
            messages.error(
                request,
                'Não é possível excluir esta categoria porque existem receitas vinculadas a ela.'
            )

        return redirect('painel:lista_categorias')

    return render(request, 'painel/categorias/excluir.html', {
        'categoria': categoria,
    })


@admin_required
def lista_ingredientes(request):
    busca = request.GET.get('q', '')

    ingredientes = Ingrediente.objects.all()

    if busca:
        ingredientes = ingredientes.filter(
            nome__icontains=busca
        )

    return render(request, 'painel/ingredientes/lista.html', {
        'ingredientes': ingredientes,
        'busca': busca,
    })


@admin_required
def criar_ingrediente(request):
    if request.method == 'POST':
        form = IngredienteForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Ingrediente cadastrado com sucesso!'
            )

            return redirect('painel:lista_ingredientes')

    else:
        form = IngredienteForm()

    return render(request, 'painel/ingredientes/formulario.html', {
        'form': form,
        'titulo': 'Novo ingrediente',
    })


@admin_required
def editar_ingrediente(request, pk):
    ingrediente = get_object_or_404(Ingrediente, pk=pk)

    if request.method == 'POST':
        form = IngredienteForm(
            request.POST,
            instance=ingrediente
        )

        if form.is_valid():
            form.save()

            messages.success(
                request,
                'Ingrediente atualizado com sucesso!'
            )

            return redirect('painel:lista_ingredientes')

    else:
        form = IngredienteForm(instance=ingrediente)

    return render(request, 'painel/ingredientes/formulario.html', {
        'form': form,
        'titulo': 'Editar ingrediente',
        'ingrediente': ingrediente,
    })


@admin_required
def excluir_ingrediente(request, pk):
    ingrediente = get_object_or_404(Ingrediente, pk=pk)

    if request.method == 'POST':
        try:
            ingrediente.delete()

            messages.success(
                request,
                'Ingrediente excluído com sucesso!'
            )

        except ProtectedError:
            messages.error(
                request,
                'Não é possível excluir este ingrediente porque ele está vinculado a uma ou mais receitas.'
            )

        return redirect('painel:lista_ingredientes')

    return render(request, 'painel/ingredientes/excluir.html', {
        'ingrediente': ingrediente,
    })