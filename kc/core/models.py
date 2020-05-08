from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='documents/', null=True)
    trailer = models.FileField(upload_to='documents/', blank=True, null=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

    # @property
    # def videos(self):
    #     return self.video_set.all()


class Driver(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        if self.name:
            return f'{self.pk},{self.name}'

        return self.pk


class Video(models.Model):
    title = models.CharField(max_length=100)
    driver = models.ForeignKey(
        Driver, default='unknown', on_delete=models.SET_DEFAULT)
    description = models.CharField(max_length=150, null=True)
    category = models.ManyToManyField(Category)
    video_file = models.FileField(upload_to='documents/', null=True)
    image_file = models.ImageField(upload_to='documents/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk},{self.title}'


class Article(models.Model):
    title = models.CharField(max_length=100)
    driver = models.ForeignKey(
        Driver, default='unknown', on_delete=models.SET_DEFAULT)
    description = models.CharField(max_length=150)
    category = models.ManyToManyField(Category)
    picture = models.ImageField(upload_to='documents/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.pk},{self.title}'


class Testimonial(models.Model):
    name = models.CharField(max_length=50)
    comment = models.TextField()
    image = models.ImageField(upload_to='documents/', null=True)

    def __str__(self):
        return self.name
