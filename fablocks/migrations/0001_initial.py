# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('slug', models.SlugField(max_length=100)),
                ('type', models.CharField(max_length=20, choices=[('container', 'Container block'), ('row', 'Row block'), ('col', 'Col block'), ('html', 'HTML block'), ('image', 'Image block')])),
                ('text', models.TextField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='fablocks/image/image/%Y/%m/%d')),
                ('blocks', models.ManyToManyField(to='fablocks.Block')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Relation',
            fields=[
                ('id', models.AutoField(primary_key=True, auto_created=True, serialize=False, verbose_name='ID')),
                ('order', models.PositiveSmallIntegerField()),
                ('child', models.ForeignKey(to='fablocks.Block', related_name='child')),
                ('parent', models.ForeignKey(to='fablocks.Block', related_name='parent')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='block',
            name='children',
            field=models.ManyToManyField(to='fablocks.Block', through='fablocks.Relation', blank=True),
            preserve_default=True,
        ),
    ]
