# Generated by Django 3.0.6 on 2021-08-21 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_category_longdescription'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='category_image',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='step1_description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='step1_title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='step2_description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='step2_title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='step3_description',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='category',
            name='step3_title',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]