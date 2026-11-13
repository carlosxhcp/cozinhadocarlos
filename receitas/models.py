from django.db import models



from django.db import models


class Receita(models.Model):

    STATUS_CHOICES = [
        ('rascunho', 'Rascunho'),
        ('publicada', 'Publicada'),
    ]

    nome = models.CharField(max_length=200, verbose_name='Nome')
    slug = models.SlugField(max_length=220, unique=True, verbose_name='Identificador')
    descricao = models.TextField(verbose_name='Descrição')

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='publicada',
        verbose_name='Status'
    )

    categoria = models.ForeignKey(
        'categorias.Categoria',
        on_delete=models.PROTECT,
        related_name='receitas',
        verbose_name='Categoria'
    )

    imagem = models.ImageField(
        upload_to='receitas/',
        blank=True,
        null=True,
        verbose_name='Imagem'
    )

    ingredientes = models.ManyToManyField(
        'ingredientes.Ingrediente',
        through='ReceitaIngrediente',
        related_name='receitas',
        verbose_name='Ingredientes'
    )

    modo_preparo = models.TextField(verbose_name='Modo de preparo')
    tempo_preparo = models.PositiveIntegerField(
        verbose_name='Tempo de preparo (minutos)'
    )
    rendimento = models.PositiveIntegerField(verbose_name='Rendimento')

    data_criacao = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Data de criação'
    )

    data_atualizacao = models.DateTimeField(
        auto_now=True,
        verbose_name='Última atualização'
    )

    class Meta:
        verbose_name = 'Receita'
        verbose_name_plural = 'Receitas'
        ordering = ['-data_criacao']

    def __str__(self):
        return self.nome



class ReceitaIngrediente(models.Model):

    receita = models.ForeignKey(
        Receita,
        on_delete=models.CASCADE,
        related_name='ingredientes_utilizados'
    )

    ingrediente = models.ForeignKey(
        'ingredientes.Ingrediente',
        on_delete=models.PROTECT,
        related_name='utilizacoes'
    )

    quantidade = models.CharField(
        max_length=100,
        verbose_name='Quantidade'
    )

    class Meta:
        verbose_name = 'Ingrediente da receita'
        verbose_name_plural = 'Ingredientes das receitas'

        constraints = [
            models.UniqueConstraint(
                fields=['receita', 'ingrediente'],
                name='ingrediente_unico_por_receita'
            )
        ]

    def __str__(self):
        return f'{self.ingrediente} - {self.quantidade}'