# Generated by Django 3.0.6 on 2020-06-30 03:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_price_product'),
        ('accounts', '0003_auto_20200629_1229'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='category',
            field=models.ForeignKey(help_text='Designates what category a user is in', null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Category'),
        ),
    ]
