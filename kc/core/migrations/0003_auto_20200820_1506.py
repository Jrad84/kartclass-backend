# Generated by Django 3.0.6 on 2020-08-20 05:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20200818_1735'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='trailer',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]