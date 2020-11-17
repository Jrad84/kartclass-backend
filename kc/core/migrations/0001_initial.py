# Generated by Django 3.0.6 on 2020-11-11 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=150)),
                ('image', models.CharField(max_length=100, null=True)),
                ('document', models.CharField(max_length=500, null=True)),
                ('likes', models.IntegerField(default=0)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Article',
                'verbose_name_plural': 'Articles',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('tier', models.CharField(max_length=50, null=True)),
                ('description', models.TextField(max_length=1000, null=True)),
                ('image', models.CharField(max_length=100, null=True)),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('trailer', models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={
                'verbose_name': 'Category',
                'verbose_name_plural': 'Categories',
            },
        ),
        migrations.CreateModel(
            name='Charge',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Testimonial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('comment', models.TextField()),
                ('image', models.CharField(max_length=500, null=True)),
            ],
            options={
                'verbose_name': 'Testimonial',
                'verbose_name_plural': 'Testimonials',
            },
        ),
        migrations.CreateModel(
            name='Video',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('longdescription', models.TextField(max_length=5000, null=True)),
                ('description', models.CharField(max_length=150, null=True)),
                ('duration', models.DecimalField(decimal_places=2, max_digits=9, null=True)),
                ('likes', models.IntegerField(default=0)),
                ('views', models.IntegerField(default=0)),
                ('video_url', models.CharField(max_length=150, null=True)),
                ('image_url_1', models.CharField(blank=True, max_length=150, null=True)),
                ('image_url_2', models.CharField(blank=True, max_length=150, null=True)),
                ('image_url_3', models.CharField(blank=True, max_length=150, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ManyToManyField(related_name='category', to='core.Category')),
            ],
            options={
                'verbose_name': 'Video',
                'verbose_name_plural': 'Videos',
            },
        ),
    ]
