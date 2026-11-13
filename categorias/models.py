from django.db import models
from django.utils.text import slugify


class Categoria(models.Model):

    nome = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nome'
    )

    slug = models.SlugField(
        max_length=120,
        unique=True,
        verbose_name='Identificador'
    )

    descricao = models.TextField(
        blank=True,
        verbose_name='Descrição'
    )

    imagem = models.ImageField(
        upload_to='categorias/',
        blank=True,
        null=True,
        verbose_name='Imagem'
    )

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['nome']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nome)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome