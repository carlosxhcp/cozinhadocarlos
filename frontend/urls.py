from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('receitas/<slug:slug>/', views.detalhe_receita, name='detalhe_receita'),
    path('buscar/', views.buscar_receitas, name='buscar_receitas'),
    path('ingredientes/sugestoes/', views.buscar_ingredientes, name='buscar_ingredientes'),
]