# Generated by Django 3.0.6 on 2020-10-10 09:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_auto_20201004_1358'),
    ]

    operations = [
       
        migrations.AlterField(
            model_name='video',
            name='image_file',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='video',
            name='video_file',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
