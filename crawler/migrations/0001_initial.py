# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-07-22 01:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dados_Ingrediente',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Ingrediente', models.CharField(max_length=150)),
                ('Receita', models.CharField(max_length=500)),
            ],
        ),
    ]
