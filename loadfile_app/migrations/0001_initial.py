# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-12 12:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='LoadFile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_name', models.CharField(blank=True, max_length=200)),
                ('file_obj', models.FileField(upload_to='media/')),
                ('str_for_search', models.CharField(max_length=200)),
            ],
        ),
    ]
