from django.db import models


class Ingrediente(models.Model):

    nome = models.CharField(
        max_length=100,
        unique=True,
        verbose_name='Nome'
    )

    class Meta:
        verbose_name = 'Ingrediente'
        verbose_name_plural = 'Ingredientes'
        ordering = ['nome']

    def __str__(self):
        return self.nome