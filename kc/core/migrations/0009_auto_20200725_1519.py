# Generated by Django 3.0.6 on 2020-07-25 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_auto_20200724_1739'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=6, null=True),
        ),
        migrations.DeleteModel(
            name='Product',
        ),
    ]