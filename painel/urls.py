from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

app_name = 'painel'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),

    path(
        'login/',
        auth_views.LoginView.as_view(
            template_name='painel/login.html',
            redirect_authenticated_user=True
        ),
        name='login'
    ),

    path(
        'logout/',
        auth_views.LogoutView.as_view(),
        name='logout'
    ),

    path('receitas/', views.lista_receitas, name='lista_receitas'),

    path(
        'receitas/nova/',
        views.criar_receita,
        name='criar_receita'
    ),

    path(
        'receitas/<int:pk>/editar/',
        views.editar_receita,
        name='editar_receita'
    ),

    path(
        'receitas/<int:pk>/excluir/',
        views.excluir_receita,
        name='excluir_receita'
    ),

    path('receitas/rascunhos/', views.lista_rascunhos, name='lista_rascunhos'),


    # Categorias
    path('categorias/', views.lista_categorias, name='lista_categorias'),

    path('categorias/nova/', views.criar_categoria, name='criar_categoria'),

    path('categorias/<int:pk>/editar/', views.editar_categoria, name='editar_categoria'),

    path('categorias/<int:pk>/excluir/', views.excluir_categoria, name='excluir_categoria'),


    # Ingredientes
    path('ingredientes/', views.lista_ingredientes, name='lista_ingredientes'),

    path('ingredientes/novo/', views.criar_ingrediente, name='criar_ingrediente'),

    path('ingredientes/<int:pk>/editar/', views.editar_ingrediente, name='editar_ingrediente'),

    path('ingredientes/<int:pk>/excluir/', views.excluir_ingrediente, name='excluir_ingrediente'),
    
]