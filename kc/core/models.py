from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, User
from django.core.validators import EmailValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField
import uuid
import stripe
from django.utils import timezone
from jsonfield.fields import JSONField
from kc.utils import CURRENCY_SYMBOLS
from django.utils.functional import cached_property
from kc.settings.base import STRIPE_SECRET_KEY, AUTH_USER_MODEL as auth_user
import json


stripe.api_key = STRIPE_SECRET_KEY


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

    class Meta:
        verbose_name: "Mail list"

    def __str__(self):
        return self.email

class Product(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=1000, null=True)
    image = models.CharField(max_length=100, null=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    quantity = models.IntegerField(null=True)
    size = models.CharField(max_length=10)

    class Meta:
        verbose_name = "Product"
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

        
class Category(models.Model):
    name = models.CharField(max_length=50)
    tier = models.CharField(max_length=50, null=True)
    description = models.TextField(max_length=1000, null=True)
    image = models.CharField(max_length=100, null=True)
    amount = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    trailer = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.name


class Video(models.Model):
    title = models.CharField(max_length=100)
    longdescription = models.TextField(max_length=5000, null=True)    
    description = models.CharField(max_length=150, null=True)
    category = models.ManyToManyField(Category, related_name='category')
    duration = models.DecimalField(decimal_places=2, max_digits=9, null=True)
    likes = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    video_url = models.CharField(max_length=150, null=True)
    image_url = models.CharField(max_length=150, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Video"
        verbose_name_plural = "Videos"

    def __str__(self):
        return self.title

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)



class Article(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=150, null=True, blank=True)
    image = models.CharField(max_length=100, null=True)
    document = models.CharField(max_length=500, null=True)
    likes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Article"
        verbose_name_plural = "Articles"

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


class Charge(models.Model):
    name = models.CharField(max_length=100, blank=True)
    