# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-13 23:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('member', '0006_auto_20170213_1150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='member',
            name='prof_pic',
            field=models.ImageField(blank=True, null=True, upload_to='prof_pic/', verbose_name='Photo Profile'),
        ),
    ]
