# Generated by Django 3.0.6 on 2020-10-24 01:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0016_delete_registration'),
    ]

    operations = [
       
        migrations.AddField(
            model_name='article',
            name='likes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='article',
            name='document',
            field=models.CharField(max_length=500, null=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='image',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='longdescription',
            field=models.TextField(max_length=4000, null=True),
        ),
    ]
