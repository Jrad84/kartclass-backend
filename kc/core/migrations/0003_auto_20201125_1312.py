# Generated by Django 3.0.6 on 2020-11-25 02:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20201125_1312'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='description',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
