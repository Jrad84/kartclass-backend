# Generated by Django 3.0.6 on 2021-05-23 05:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_customuser_mail_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='temp_cat',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
