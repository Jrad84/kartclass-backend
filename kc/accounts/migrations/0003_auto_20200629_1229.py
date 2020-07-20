# Generated by Django 3.0.6 on 2020-06-29 02:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_price_product'),
        ('accounts', '0002_userstripe'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Category'),
        ),
        migrations.DeleteModel(
            name='UserStripe',
        ),
    ]
