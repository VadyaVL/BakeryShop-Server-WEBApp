# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-23 21:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BakeryShop', '0004_auto_20161123_2345'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Description',
            field=models.TextField(db_column=b'Description', verbose_name=b'\xd0\x9e\xd0\xbf\xd0\xb8\xd1\x81'),
        ),
    ]