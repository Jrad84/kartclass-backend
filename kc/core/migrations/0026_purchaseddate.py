# Generated by Django 3.2.7 on 2021-11-17 02:59

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0025_worksheet'),
    ]

    operations = [
        migrations.CreateModel(
            name='PurchasedDate',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(error_messages={'unique': 'A user with that email already exists.'}, max_length=254, validators=[django.core.validators.EmailValidator()], verbose_name='email address')),
                ('purchased', models.DateTimeField()),
                ('category', models.ManyToManyField(related_name='purchased_category', to='core.Category')),
            ],
            options={
                'verbose_name': 'PurchasedDate',
                'verbose_name_plural': 'PurchasedDate',
            },
        ),
    ]
