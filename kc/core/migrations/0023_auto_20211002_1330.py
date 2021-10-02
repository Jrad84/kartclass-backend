# Generated by Django 3.0.6 on 2021-10-02 03:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_podcast'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='category',
            field=models.ManyToManyField(related_name='article_category', to='core.Category'),
        ),
        migrations.RemoveField(
            model_name='podcast',
            name='category',
        ),
        migrations.AddField(
            model_name='podcast',
            name='category',
            field=models.ManyToManyField(related_name='podcast_category', to='core.Category'),
        ),
        migrations.AlterField(
            model_name='video',
            name='category',
            field=models.ManyToManyField(related_name='video_category', to='core.Category'),
        ),
    ]
