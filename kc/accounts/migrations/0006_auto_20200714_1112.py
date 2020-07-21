# Generated by Django 3.0.6 on 2020-07-14 01:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_customuser_stripe_token'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='stripe_token',
        ),
        migrations.AddField(
            model_name='customuser',
            name='stripe_id',
            field=models.CharField(blank=True, help_text='Stripe user id', max_length=300, null=True),
        ),
    ]