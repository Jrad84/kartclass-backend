from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.core.validators import EmailValidator
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
import uuid
from jsonfield.fields import JSONField
from django.utils.functional import cached_property
from kc.settings.base import AUTH_USER_MODEL as auth_user
import json


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

class MailList(models.Model):
    email_validator = EmailValidator()
    email = models.EmailField(
        _("email address"),
        unique=True,
        validators=[email_validator],
        error_messages={"unique": _("A user with that email already exists.")}, 
    )

    # class Meta:
    #     verbose_name: "Mail list"

    def __str__(self):
        return self.email

class Product(models.Model):
    name = models.CharField(max_length=50)
    slug = models.SlugField(max_length=100, null=True, unique=True)
    description = models.TextField(max_length=1000, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    stock_level = models.IntegerField(null=True)
    size = models.CharField(max_length=10)
    image1_url = models.CharField(max_length=150, null=True, blank=True)
    image2_url = models.CharField(max_length=150, null=True, blank=True)
    
    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

        
class Category(models.Model):
    name = models.CharField(max_length=50)
    shopify_id = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=100, null=True, unique=True)
    sort = models.IntegerField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    tier = models.CharField(max_length=50, null=True)
    description = models.TextField(max_length=1000, null=True)
    longdescription = models.TextField(max_length=1000, null=True)
    step1_title  = models.CharField(max_length=50, null=True, blank=True)
    step1_description  = models.CharField(max_length=200, null=True, blank=True)
    step2_title  = models.CharField(max_length=50, null=True, blank=True)
    step2_description  = models.CharField(max_length=200, null=True, blank=True)
    step3_title  = models.CharField(max_length=50, null=True, blank=True)
    step3_description  = models.CharField(max_length=200, null=True, blank=True)
    image = models.CharField(max_length=100, null=True)
    category_image = models.CharField(max_length=100, null=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    trailer = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def save(self, *args, **kwargs):
        value = self.name
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Blog(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=True, unique=True)
    body = models.TextField(max_length=9000)
    author = models.CharField(max_length=100)
    image_url = models.CharField(max_length=150, null=True, blank=True)
    seo_tags = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Blog"
        verbose_name_plural = "Blogs"
    
    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title



class Video(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=True, unique=True)
    longdescription = models.TextField(max_length=9000, null=True)    
    description = models.CharField(max_length=150, null=True)
    category = models.ManyToManyField(Category, related_name='video_category')
    duration = models.DecimalField(decimal_places=2, max_digits=9, null=True)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    video_high_url = models.CharField(max_length=150, null=True)
    video_low_url = models.CharField(max_length=150, null=True)
    image1_url = models.CharField(max_length=150, null=True, blank=True)
    image2_url = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    document = models.CharField(max_length=500, null=True, blank=True)

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)
   
    def __str__(self):
        return self.title

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)


class Article(models.Model):
    title = models.CharField(max_length=100)
    category = models.ManyToManyField(Category, related_name='article_category')
    slug = models.SlugField(max_length=100, null=True, unique=True)
    description = models.CharField(max_length=150, null=True, blank=True)
    image = models.CharField(max_length=100, null=True)
    document = models.CharField(max_length=500, null=True)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Testimonial(models.Model):
    name = models.CharField(max_length=50)
    comment = models.TextField()
    image = models.CharField(max_length=500, null=True)

    class Meta:
        verbose_name = "Testimonial"
        verbose_name_plural = "Testimonials"

    def __str__(self):
        return self.name


class Podcast(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, null=True, unique=True)
    category = models.ManyToManyField(Category, related_name='podcast_category')
    longdescription = models.TextField(max_length=9000, null=True)    
    description = models.CharField(max_length=150, null=True)
    duration = models.DecimalField(decimal_places=2, max_digits=9, null=True)
    image = models.CharField(max_length=100, null=True)
    video_high_url = models.CharField(max_length=500, null=True)
    likes = models.IntegerField(default=0)
    listens = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Podcast"
        verbose_name_plural = "Podcasts"

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Charge(models.Model):
    name = models.CharField(max_length=100, blank=True)


class Worksheet(models.Model):
    title = models.CharField(max_length=100)
    category = models.ManyToManyField(Category, related_name='worksheet_category')
    slug = models.SlugField(max_length=100, null=True, unique=True)
    description = models.CharField(max_length=150, null=True, blank=True)
    image = models.CharField(max_length=100, null=True)
    document = models.CharField(max_length=500, null=True)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Worksheet"
        verbose_name_plural = "Worksheet"

    def save(self, *args, **kwargs):
        value = self.title
        self.slug = slugify(value, allow_unicode=True)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title