# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-23 21:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('BakeryShop', '0002_shop'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Title', models.CharField(db_column=b'Title', max_length=100, verbose_name=b'\xd0\x9d\xd0\xb0\xd0\xb7\xd0\xb2\xd0\xb0')),
                ('Description', models.CharField(db_column=b'Description', max_length=1000, verbose_name=b'\xd0\x9e\xd0\xbf\xd0\xb8\xd1\x81')),
                ('Photo', models.CharField(db_column=b'Photo', max_length=1000, verbose_name=b'\xd0\xa4\xd0\xbe\xd1\x82\xd0\xbe')),
                ('Price', models.FloatField(db_column=b'Price', verbose_name=b'\xd0\xa6\xd1\x96\xd0\xbd\xd0\xb0')),
            ],
            options={
                'db_table': 'Product',
            },
        ),
    ]
