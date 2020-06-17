from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
import uuid


class Base(models.Model):
    """Base model.
    Contains fields:
    - `date_created`
    - `date_updated`
    """

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Uuid(models.Model):
    """UUID model.
    Contains fields:
    - `uuid`
    """

    uuid = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True, verbose_name="UUID"
    )

    class Meta:
        abstract = True

        
class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=100, null=True)
    image = models.ImageField(upload_to='documents/', null=True)
    trailer = models.FileField(upload_to='documents/', blank=True, null=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name

    # @property
    # def videos(self):
    #     return self.video_set.all()


class Driver(models.Model):
    name = models.CharField(max_length=50)

    class Meta:
        verbose_name = "Driver"
        verbose_name_plural = "Drivers"

    def __str__(self):
         return self.name



class Video(models.Model):
    title = models.CharField(max_length=100)
    driver = models.ForeignKey(
        Driver, default='unknown', on_delete=models.SET_DEFAULT)
    description = models.CharField(max_length=150, null=True)
    category = models.ManyToManyField(Category, related_name='category')
    video_file = models.FileField(upload_to='documents/', null=True)
    image_file = models.ImageField(upload_to='documents/', null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=100)
    driver = models.ForeignKey(
        Driver, default='unknown', on_delete=models.SET_DEFAULT)
    description = models.CharField(max_length=150)
    category = models.ManyToManyField(Category)
    picture = models.ImageField(upload_to='documents/', null=True)
    text = models.TextField(default="textarea")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=50)
    comment = models.TextField()
    image = models.ImageField(upload_to='documents/', null=True)

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return self.name
