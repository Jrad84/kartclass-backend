# Generated by Django 3.0.6 on 2020-11-09 02:15

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_auto_20201027_2031'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='videos',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='category',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.IntegerField(), default=list, null=True, size=None),
        ),
    ]
