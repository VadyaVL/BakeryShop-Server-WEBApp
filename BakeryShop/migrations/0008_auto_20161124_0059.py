# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-23 22:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BakeryShop', '0007_auto_20161124_0057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='Photo',
            field=models.ImageField(db_column=b'Photo', upload_to=b'', verbose_name=b'\xd0\xa4\xd0\xbe\xd1\x82\xd0\xbe'),
        ),
    ]