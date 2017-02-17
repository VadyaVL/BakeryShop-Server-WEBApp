# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-11-28 21:47
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('BakeryShop', '0008_auto_20161124_0059'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProductToShop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Product_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BakeryShop.Product')),
            ],
            options={
                'db_table': 'ProductToShop',
            },
        ),
        migrations.CreateModel(
            name='SendToShop',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('DateTime', models.DateTimeField(db_column=b'DateTime', verbose_name=b'\xd0\xa7\xd0\xb0\xd1\x81 \xd0\xb4\xd0\xbe\xd1\x81\xd1\x82\xd0\xb0\xd0\xb2\xd0\xba\xd0\xb8')),
                ('Shop_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BakeryShop.Shop')),
                ('User_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'SendToShop',
            },
        ),
        migrations.AddField(
            model_name='producttoshop',
            name='SendToShop_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BakeryShop.SendToShop'),
        ),
    ]
