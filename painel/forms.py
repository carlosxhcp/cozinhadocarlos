
from django import forms
from django.forms import inlineformset_factory

from receitas.models import Receita, ReceitaIngrediente
from categorias.models import Categoria
from ingredientes.models import Ingrediente


class ReceitaForm(forms.ModelForm):

    # Permite gerar o slug automaticamente caso fique vazio.
    slug = forms.SlugField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'frango-empanado',
        })
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['categoria'].empty_label = ''

    class Meta:
        model = Receita

        fields = [
            'nome',
            'slug',
            'descricao',
            'categoria',
            'imagem',
            'modo_preparo',
            'tempo_preparo',
            'rendimento',
        ]

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: Frango empanado',
            }),

            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descreva brevemente a receita',
            }),

            'categoria': forms.Select(attrs={
                'class': 'form-select tom-select',
                'data-placeholder': 'Pesquisar categoria...',
            }),

            'imagem': forms.ClearableFileInput(attrs={
                'class': 'form-control',
            }),

            'modo_preparo': forms.Textarea(attrs={
                'class': 'form-control',
                'id': 'editor-modo-preparo',
                'placeholder': 'Descreva o passo a passo...',
            }),

            'tempo_preparo': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
            }),

            'rendimento': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': 1,
            }),
        }


class ReceitaIngredienteForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['ingrediente'].empty_label = ''
    class Meta:
        model = ReceitaIngrediente

        fields = [
            'ingrediente',
            'quantidade',
        ]

        widgets = {
            'ingrediente': forms.Select(attrs={
                'class': 'form-select tom-select',
                'data-placeholder': 'Pesquisar ingrediente...',
            }),

            'quantidade': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: 500 g, 2 unidades',
            }),
        }


ReceitaIngredienteFormSet = inlineformset_factory(
    Receita,
    ReceitaIngrediente,
    form=ReceitaIngredienteForm,
    extra=1,
    can_delete=True,
)


class CategoriaForm(forms.ModelForm):

    slug = forms.SlugField(
    required=False,
    widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'sobremesas',
    })
)

    class Meta:
        model = Categoria

        fields = [
            'nome',
            'slug',
            'descricao',
            'imagem',
        ]

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: Sobremesas',
            }),

            'slug': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'sobremesas',
            }),

            'descricao': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Descrição da categoria',
            }),

            'imagem': forms.ClearableFileInput(attrs={
                'class': 'form-control image-input',
                'accept': 'image/*',
            }),
        }



class IngredienteForm(forms.ModelForm):

    class Meta:
        model = Ingrediente

        fields = [
            'nome',
        ]

        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ex.: Farinha de trigo',
            }),
        }