# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-09-03 08:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rango', '0006_category_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
    ]