# Generated by Django 3.0.6 on 2021-04-14 05:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20210401_1530'),
    ]

    operations = [
        migrations.RenameField(
            model_name='video',
            old_name='image_url',
            new_name='image1_url',
        ),
        migrations.AddField(
            model_name='video',
            name='image2_url',
            field=models.CharField(blank=True, max_length=150, null=True),
        ),
    ]
