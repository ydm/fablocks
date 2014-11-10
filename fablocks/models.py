# -*- coding: utf-8 -*-

from django.db import models


def order_next(parent_block):
    d = Relation.objects.filter(parent=parent_block).aggregate(
        models.Max('order')
    )
    order = d['order__max']
    return 1 + (order or 0)


class Relation(models.Model):

    parent = models.ForeignKey('Block', related_name='parent')
    child = models.ForeignKey('Block', related_name='child')
    order = models.PositiveSmallIntegerField()

    # def save(self, *args, **kwargs):
    #     if self.order is None:
    #         self.order = order_next(self.parent)
    #     return super(Relation, self).save(*args, **kwargs)


class Block(models.Model):

    TYPE_CHOICES = (
        # Grid blocks
        ('container', 'Container block'),
        ('row', 'Row block'),
        ('col', 'Col block'),

        ('html', 'HTML block'),
        ('image', 'Image block'),
    )

    slug = models.SlugField(max_length=100, unique=True)
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    text = models.TextField(blank=True)
    children = models.ManyToManyField(
        'self',                 # Blocks may aggregate blocks
        blank=True,             # A block may not have any children
        symmetrical=False,      # It's not symmetrical obviously
        through=Relation        # We need to keep order of children
    )

    def __str__(self):
        return self.slug


class Image(models.Model):

    blocks = models.ManyToManyField(Block)
    image = models.ImageField(upload_to='fablocks/image/image/%Y/%m/%d')
